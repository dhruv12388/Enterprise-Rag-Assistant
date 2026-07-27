import os
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models


class VectorStoreService:
    def __init__(self, collection_name: str = "documents"):
        self.collection_name = collection_name

        # Qdrant configuration
        self.qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        self.qdrant_port = int(os.getenv("QDRANT_PORT", 6333))

        # Google Gemini API key setup
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing Gemini API key. Ensure GEMINI_API_KEY is defined in your backend/.env file."
            )

        # Initialize Google Generative AI Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )

        # Initialize Qdrant Client
        self.client = QdrantClient(host=self.qdrant_host, port=self.qdrant_port)
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Creates the Qdrant collection if it does not already exist."""
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            # Note: models/embedding-001 produces 768-dimensional vectors
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=768,
                    distance=models.Distance.COSINE
                )
            )

    def add_texts(self, texts: list[str], metadatas: list[dict] = None) -> list[str]:
        """Embeds text chunks and stores them in Qdrant vector database."""
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
        return vector_store.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search(self, query: str, top_k: int = 4):
        """Searches Qdrant for document chunks relevant to the user query."""
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
        return vector_store.similarity_search(query=query, k=top_k)


# Helper functions to support direct functional imports in endpoints
def store_document_chunks(chunks: list[str], metadatas: list[dict] = None):
    """Wrapper function imported by documents.py route."""
    service = VectorStoreService()
    return service.add_texts(texts=chunks, metadatas=metadatas)


def search_documents(query: str, top_k: int = 4):
    """Wrapper function for searching documents."""
    service = VectorStoreService()
    return service.similarity_search(query=query, top_k=top_k)