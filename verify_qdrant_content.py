import os
import logging
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables from backend/.env
dotenv_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
load_dotenv(dotenv_path=dotenv_path)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLLECTION_NAME = "physical_ai_book"
BATCH_SIZE = 100

def get_qdrant_client():
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in environment.")

    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=30)
    client.get_collections()  # Health check
    logger.info("✅ Connected to Qdrant")
    return client

def extract_sample_content(client: QdrantClient):
    logger.info("Fetching sample points to inspect payload structure...")
    records, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=20,
        with_payload=True,
        with_vectors=False
    )

    print("\n=== SAMPLE PAYLOAD STRUCTURES ===")
    unique_keys = set()
    for i, record in enumerate(records[:10]):
        print(f"\n--- Point {i+1} (ID: {record.id}) ---")
        if record.payload:
            print("Payload keys:", list(record.payload.keys()))
            for key, value in record.payload.items():
                unique_keys.add(key)
                if isinstance(value, str) and len(value) < 300:
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {str(value)[:300]}..." if value else "  (empty)")
        else:
            print("No payload!")

    print("\n=== ALL UNIQUE PAYLOAD KEYS FOUND ===")
    print(sorted(unique_keys))

    text_candidates = ['page_content', 'text', 'content', 'chunk', 'document']
    print("\n=== LOOKING FOR TEXT CONTENT ===")
    for record in records:
        for key in text_candidates:
            if key in record.payload and record.payload[key]:
                print(f"Found text in '{key}': {record.payload[key][:200]}...")
                return

if __name__ == "__main__":
    try:
        client = get_qdrant_client()
        extract_sample_content(client)
    except Exception as e:
        logger.error(f"Error: {e}")