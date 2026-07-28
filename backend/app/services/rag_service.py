from app.config import settings

async def query_rag_pipeline(user_query: str, top_k: int = 4) -> dict:
    try:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',  
            contents=f"Answer the following question clearly and helpfully: {user_query}"
        )
        return {
            "answer": response.text,
            "sources": []
        }
    except Exception as e:
        # This will print the real reason in your Render logs
        print(f"CRITICAL GEMINI API ERROR: {str(e)}")
        
        # Return the exact error to the UI temporarily so you can see what's wrong
        return {
            "answer": f"Gemini Error: {str(e)}",
            "sources": []
        }
