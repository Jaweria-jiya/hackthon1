import sys
import os
import re

# Add the parent directory to the path to allow importing reasoning_engine
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reasoning_engine import chat

# Define a set of validation questions and expected outcomes.
# For a real-world scenario, this would be more extensive and might include
# checking for specific source documents.
VALIDATION_SET = [
    {
        "question": "What is ROS 2?",
        "expected_keywords": ["Robot Operating System", "framework", "middleware"],
        "expected_citation_pattern": r"[Source:.*what-is-ros-2.md.*]" # Regex pattern
    },
    {
        "question": "What is a digital twin?",
        "expected_keywords": ["virtual model", "real-world", "simulation", "synchronization"],
        "expected_citation_pattern": r"[Source:.*the-concept-of-a-digital-twin.md.*]"
    },
    {
        "question": "What is NVIDIA Isaac Sim?",
        "expected_keywords": ["NVIDIA", "robotics", "simulation", "platform", "Omniverse"],
        "expected_citation_pattern": r"[Source:.*isaac-sim.md.*]"
    },
    {
        "question": "How does a Vision-Language-Action (VLA) model work?",
        "expected_keywords": ["vision", "language", "action", "multimodal", "robot"],
        "expected_citation_pattern": r"[Source:.*what-is-vla.md.*]"
    }
]

def validate_rag_system():
    """
    Runs a set of validation checks on the RAG system.
    """
    print("--- Starting RAG System Validation ---")
    
    all_passed = True
    
    for i, item in enumerate(VALIDATION_SET):
        print(f"\n--- Test Case {i+1} ---")
        question = item["question"]
        expected_keywords = item["expected_keywords"]
        expected_citation_pattern = item["expected_citation_pattern"]
        
        print(f"Question: {question}")
        
        # Get the response from the chat function
        response = chat(question)
        
        passed_keyword_check = False
        passed_citation_check = False

        if "Sorry, I encountered an error" in response:
            print("Chat function returned an error message. Skipping keyword and citation checks.")
            # Since the underlying services are not running/configured, this test fails.
            all_passed = False
        else:
            # Only perform checks if the response is not an error message
            passed_keyword_check = all(keyword.lower() in response.lower() for keyword in expected_keywords)
            
            citation_match = re.search(expected_citation_pattern, response)
            passed_citation_check = citation_match is not None
            
            if not passed_keyword_check or not passed_citation_check:
                all_passed = False
        
        print(f"Response: {response}")
        print(f"Keyword check passed: {passed_keyword_check}")
        print(f"Citation check passed: {passed_citation_check}")
        
        if not passed_keyword_check or not passed_citation_check: # Re-evaluate condition after potential skip
            print("--- FAILED ---")
        else:
            print("--- PASSED ---")

    print("\n--- RAG System Validation Summary ---")
    if all_passed:
        print("All validation tests passed successfully!")
    else:
        print("Some validation tests failed.")

if __name__ == "__main__":
    # Note: This script assumes that the backend FastAPI server with the retrieval API is running.
    # It also assumes the Qdrant database has been populated by running the ingest_pipeline.
    validate_rag_system()