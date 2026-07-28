from google import genai
from app.config import settings

# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def query_rag_pipeline(user_query: str, top_k: int = 4) -> str:
    """
    Executes the RAG pipeline using Gemini.
    (Currently this is only an LLM call. Retrieval from Qdrant should be added later.)
    """
    try:
        prompt = f"""
You are an Enterprise AI Assistant.

Answer the following question as accurately as possible.

Question:
{user_query}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if response.text:
            return response.text

        return "No response generated."

    except Exception as e:
        print(f"Gemini Error: {e}")
        raise Exception(str(e))
