from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Models to try in order
MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

def query_rag_pipeline(user_query: str, top_k: int = 4) -> str:
    prompt = f"""
You are an Enterprise RAG Assistant.

Answer the following question accurately.

Question:
{user_query}
"""

    last_error = None

    for model_name in MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            if hasattr(response, "text") and response.text:
                return response.text

        except Exception as e:
            last_error = e
            continue

    raise Exception(
        f"No supported Gemini model found for this API key.\nLast error: {last_error}"
    )
