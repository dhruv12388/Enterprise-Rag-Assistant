from google import genai
from app.config import settings

# Initialize the Gemini client explicitly using your settings API key
client = genai.Client(api_key=settings.GEMINI_API_KEY)

def query_rag_pipeline(user_query: str, top_k: int = 4) -> str:
    """
    Executes the RAG pipeline query using the Google GenAI SDK.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',  # Updated to the active supported model ID
            contents=f"Answer this query accurately based on your knowledge base (retrieve up to {top_k} results): {user_query}"
        )
        return response.text
    except Exception as e:
        print(f"Error executing RAG pipeline with Gemini: {e}")
        raise e
