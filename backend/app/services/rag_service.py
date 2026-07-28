from app.config import settings
import os
from groq import Groq

async def query_rag_pipeline(user_query: str, top_k: int = 4) -> dict:
    """
    Dynamically calls Groq to generate a unique ChatGPT-like response 
    using Llama 3.
    """
    try:
        # Initialize the Groq client (ensure your environment variable is named GROQ_API_KEY)
        client = Groq(api_key=os.getenv("GROQ_API_KEY", settings.GEMINI_API_KEY))
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Nexus AI, a helpful, intelligent enterprise assistant."
                },
                {
                    "role": "user",
                    "content": user_query,
                }
            ],
            model="llama-3.3-70b-versatile", # High-performance open model available on Groq
        )
        
        answer_text = chat_completion.choices[0].message.content
    except Exception as e:
        answer_text = f"Groq Error: {str(e)}"

    return {
        "answer": answer_text,
        "sources": []
    }
