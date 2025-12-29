import os
import uuid
import time
from typing import List, Dict, Generator
import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys


# --- Configuration ---

# File Paths
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_SCRIPT_DIR, "../../"))
DOCS_DIR = os.path.join(_PROJECT_ROOT, "frontend-docusaurus/website/docs")



# Load environment variables from backend/.env
backend_env_path = os.path.join(_PROJECT_ROOT, "backend", ".env")
if not os.path.exists(backend_env_path):
    print(f"FATAL: Environment file not found at {backend_env_path}")
    sys.exit(1)
load_dotenv(dotenv_path=backend_env_path)



# Chunking Parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200



# OpenAI Embedding Model

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
openai.api_key = OPENAI_API_KEY
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSION = 3072



# Qdrant Configuration

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_book")



if not QDRANT_URL:

    raise ValueError("QDRANT_URL environment variable not set.")



# Batch size for uploading to Qdrant



BATCH_SIZE = 16





# --- Core Functions ---



def read_book_files(directory: str) -> List[Dict]:

    """

    Reads all supported files (.md, .mdx, .txt, .pdf) from a directory.

    """

    documents = []

    for root, _, files in os.walk(directory):

        for file in files:

            filepath = os.path.join(root, file)

            relative_path = os.path.relpath(filepath, directory)

            content = ""



            try:

                if file.endswith((".md", ".mdx", ".txt")):

                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:

                        content = f.read()

                elif file.endswith(".pdf"):

                    with fitz.open(filepath) as pdf_file:

                        content = "".join(page.get_text() for page in pdf_file)

                else:

                    continue  # Skip unsupported file types



                if content:

                    documents.append({

                        "content": content,

                        "metadata": {"source": relative_path}

                    })

            except Exception as e:

                print(f"Error reading {filepath}: {e}")



    return documents



def chunk_documents(documents: List[Dict]) -> List[Dict]:

    """

    Splits documents into smaller chunks with metadata.

    """

    text_splitter = RecursiveCharacterTextSplitter(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        length_function=len,

    )

    

    chunks = []

    for doc in documents:

        split_texts = text_splitter.split_text(doc["content"])

        chapter_name = os.path.splitext(os.path.basename(doc["metadata"]["source"] or ""))[0]



        for i, text in enumerate(split_texts):

            chunks.append({

                "content": text,

                "metadata": {

                    **doc["metadata"],

                    "chunk_id": f"{doc['metadata']['source']}_{i}",

                    "chunk_index": i,

                    "chapter": chapter_name,

                }

            })

    return chunks


def generate_embeddings_batch(texts: List[str], max_retries: int = 5, initial_delay: float = 1.0, timeout: int = 30) -> List[List[float]]:


    """


    Generates embeddings for a batch of texts using OpenAI's API with robust retry logic.


    Handles transient network issues with exponential backoff.


    """


    delay = initial_delay


    for attempt in range(max_retries):


        try:


            # Add a timeout to the request


            response = openai.embeddings.create(


                input=texts, 


                model=EMBEDDING_MODEL,


                timeout=timeout


            )


            return [item.embedding for item in response.data]


        # Catch connection errors that are likely to be transient


        except openai.APIConnectionError as e:


            print(f"🟡 OpenAI API connection error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {delay:.2f}s...")


            time.sleep(delay)


            delay *= 2  # Exponential backoff


        # Catch other unexpected errors


        except Exception as e:


            print(f"🔴 An unexpected error occurred during embedding generation: {e}")


            raise





    # If all retries fail, raise an exception to halt the process for this batch


    error_message = f"Failed to generate embeddings after {max_retries} retries."


    print(f"🔴 {error_message}")


    raise Exception(error_message)

def batch_generator(data: List, batch_size: int) -> Generator[List, None, None]:

    """Yields successive n-sized chunks from a list."""

    for i in range(0, len(data), batch_size):

        yield data[i:i + batch_size]

def upload_to_qdrant(client: QdrantClient, chunks: List[Dict]):
    """
    Generates embeddings and uploads data to Qdrant in batches with retry logic.
    """
    print(f"Generating and uploading {len(chunks)} chunks in batches of {BATCH_SIZE}...")
    
    max_retries = 3
    retry_delay_seconds = 5 # 5 seconds delay between retries

    for i, batch in enumerate(batch_generator(chunks, BATCH_SIZE)):
        print(f"Processing batch {i + 1} (size: {len(batch)})...")
        
        # Extract content for embedding
        contents = [item["content"] for item in batch]
        
        # Generate embeddings
        embeddings = generate_embeddings_batch(contents)
        
        points_to_upsert = [
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[j],
                payload={
                    "content": contents[j],
                    **batch[j]["metadata"]
                }
            )
            for j in range(len(batch))
        ]

        for attempt in range(max_retries):
            try:
                # Upload to Qdrant
                client.upsert(
                    collection_name=QDRANT_COLLECTION_NAME,
                    points=points_to_upsert,
                    wait=True  # Wait for the operation to complete
                )
                print(f"✅ Successfully uploaded batch {i + 1} on attempt {attempt + 1}.")
                break # Break from retry loop if successful
            except Exception as e:
                print(f"❌ Failed to upload batch {i + 1} on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying batch {i + 1} in {retry_delay_seconds} seconds...")
                    time.sleep(retry_delay_seconds)
                else:
                    print(f"🔴 Max retries reached for batch {i + 1}. This batch failed to upload.")
    print("All batches processed (some might have failed after retries).")

def test_retrieval(query_text: str, client: QdrantClient):
    print(f"\n--- Testing Retrieval for: '{query_text}' ---")
    
    # Generate embedding for query
    query_vector = generate_embeddings_batch([query_text])[0]
    
    points_from_query = []
    
    try:
        query_response = client.query_points(
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_vector,
            limit=5,
            with_payload=True
        )
        points_from_query = query_response.points
        print(f"✅ Qdrant search returned {len(points_from_query)} points for '{query_text}'.")
    except Exception as e:
        print(f"ERROR: Qdrant search failed during test retrieval for '{query_text}': {e}")
        points_from_query = [] # Ensure it defaults to an empty list on failure
    
    if points_from_query:
        print("Retrieved Context:")
        for hit in points_from_query:
            # Safely access payload: check if it's an object with .payload or a dict
            payload = {}
            score = 'N/A'
            
            if hasattr(hit, 'payload') and hit.payload is not None:
                payload = hit.payload
            
            if hasattr(hit, 'score') and hit.score is not None:
                score = hit.score
            
            print(
                f"- Score: {score:.2f}, "
                f"Source: {payload.get('source')}, "
                f"Chapter: {payload.get('chapter')}, "
                f"Chunk: {payload.get('chunk_index')}"
            )
            print(f"  Content: {payload.get('content', '')[:200].strip()}...")
    else:
        print("No relevant chunks found.")
    
    print("--- Retrieval Test Complete ---")

def main():
    """
    Main function to run the ingestion pipeline.
    """
    print(f"Starting ingestion pipeline from '{DOCS_DIR}'...")
    
    # 1. Read files
    documents = read_book_files(DOCS_DIR)
    if not documents:
        print("No documents found. Exiting.")
        return
    print(f"Found {len(documents)} documents.")
    
    # 2. Chunk documents
    chunks = chunk_documents(documents)
    print(f"Generated {len(chunks)} chunks.")
    
    # 3. Set up Qdrant client
    print(f"Resolved QDRANT_URL: {QDRANT_URL}")
    if "localhost" in QDRANT_URL:
        print("FATAL: QDRANT_URL points to localhost. Aborting.")
        sys.exit(1)

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # 4. Ensure Qdrant collection exists
    print(f"Validating existence of collection '{QDRANT_COLLECTION_NAME}'...")
    try:
        collection_info = client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' found.")
    except Exception as e:
        print(f"FATAL: Collection '{QDRANT_COLLECTION_NAME}' not found or could not be accessed.")
        print(f"Error: {e}")
        sys.exit(1)

    # 5. Generate embeddings and upload to Qdrant
    upload_to_qdrant(client, chunks)
    
    # 6. Verification and Final Report
    print("\n--- FINAL STATUS REPORT ---")
    try:
        collection_info = client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        points_count = collection_info.points_count
        
        print(f"QDRANT_URL actually used: {QDRANT_URL}")
        print(f"Collection name used: {QDRANT_COLLECTION_NAME}")
        print(f"Number of documents loaded: {len(documents)}")
        print(f"Number of chunks created: {len(chunks)}")
        print(f"Number of vectors stored: {points_count}")
        
        if points_count > 0:
            print("RAG status: ACTIVE")
            test_retrieval("What is the architecture of ROS 2?", client)
        else:
            print("RAG status: FAILED - No vectors were stored.")
            
    except Exception as e:
        print("RAG status: FAILED - Could not retrieve final collection stats.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()