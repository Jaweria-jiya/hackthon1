import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file in the current directory
load_dotenv()

# Configure the Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please create an .env file in the 'agents-openai' directory.")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')

def translate_content_to_urdu(content: str) -> str:
    """
    Translates the given content to Urdu using the Gemini API.

    Args:
        content: The text content (can be markdown or HTML) to translate.

    Returns:
        The translated Urdu text.
    """
    if not content:
        return ""

    try:
        # The prompt is carefully crafted to handle various content types and provide a direct translation.
        prompt = f"You are an expert translator. Translate the following content accurately into Urdu. Preserve the original formatting (like markdown or HTML tags) as much as possible. Do not add any extra explanations, just provide the translated text.\n\nCONTENT TO TRANSLATE:\n---\n{content}\n---\n\nTRANSLATED URDU:"
        
        response = model.generate_content(prompt)
        
        # Accessing the translated text safely
        if response.parts:
            translated_text = response.text
        else:
            # Handle cases where the response might be blocked or empty
            # See safety feedback details in response.prompt_feedback
            print(f"Warning: Gemini response was empty or blocked. Feedback: {response.prompt_feedback}")
            return "Translation failed due to safety settings or an empty response."

        return translated_text.strip()

    except Exception as e:
        print(f"An error occurred during Gemini API call: {e}")
        # In a real app, you might want more robust error handling or logging
        return "An error occurred during translation."

if __name__ == '__main__':
    # Example usage for testing
    sample_content = """
    ## Chapter 1: The Concept of a Digital Twin

    A digital twin is a virtual model designed to accurately reflect a physical object. 
    The object being studied – for example, a wind turbine – is outfitted with various sensors related to vital areas of functionality.
    
    *   Sensor data is processed.
    *   A virtual model is created.
    
    This is an important concept in modern engineering.
    """
    print("--- Testing Urdu Translation Agent ---")
    translated = translate_content_to_urdu(sample_content)
    print("\nOriginal Content:\n", sample_content)
    print("\nTranslated Content:\n", translated)
    print("\n--- Test Complete ---")
