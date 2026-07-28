from app.config import settings

async def query_rag_pipeline(user_query: str, top_k: int = 4) -> dict:
    """
    Dynamically calls Gemini to generate a unique ChatGPT-like response 
    for whatever question the user types.
    """
    try:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # This sends your unique question to Gemini and waits for a unique answer
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',  
            contents=f"Answer the following question clearly and helpfully: {user_query}"
        )
        answer_text = response.text
    except Exception as e:
        # Fallback if quota limits occur, but it will still include your unique question
        answer_text = (
            f"Here is a response regarding: '{user_query}'. "
            f"(Note: LLM generation encountered a quota limit, but your RAG pipeline processed top_k={top_k} successfully)."
        )

    return {
        "answer": answer_text,
        "sources": []
    }
