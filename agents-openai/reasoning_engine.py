import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# Import BookRAGAssistant
from backend.app.agents.book_rag_agent import BookRAGAssistant

# Load environment variables
load_dotenv()

# Initialize BookRAGAssistant
book_rag_agent = BookRAGAssistant()

def chat(query: str):
    """
    Main chat function to orchestrate the RAG process using BookRAGAssistant.
    """
    print(f"Received query: {query}")

    # Get answer from the agent
    print("Getting response from agent...")
    answer = book_rag_agent.generate_answer(query)
    print(f"\n--- RESPONSE ---\n{answer}\n--- END RESPONSE ---\n")
    
    return answer

if __name__ == '__main__':
    # Example usage
    example_query = "What is ROS 2?"
    chat(example_query)
