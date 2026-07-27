import io
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.schemas.document import QueryRequest, QueryResponse
from app.services.vector_store import store_document_chunks
from app.services.rag_service import query_rag_pipeline

router = APIRouter()


# ==========================================
# 1. Document Upload & Ingestion Endpoint
# ==========================================
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Extracts text from uploaded PDF or TXT files, splits the text into 
    overlapping chunks, and stores the vector embeddings in Qdrant.
    """
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only PDF and TXT files are supported."
        )

    try:
        # Read uploaded file content
        content = await file.read()
        extracted_text = ""

        # Extract text based on file extension
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                extracted_text += page.extract_text() or ""
        else:
            extracted_text = content.decode("utf-8")

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Could not extract any readable text from the document."
            )

        # Chunk the extracted text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        chunks = text_splitter.split_text(extracted_text)

        # Store vectors into Qdrant vector database
        await store_document_chunks(chunks=chunks, filename=file.filename, user_id=1)

        return {
            "status": "success",
            "filename": file.filename,
            "total_chunks_indexed": len(chunks)
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the document: {str(e)}"
        )


# ==========================================
# 2. RAG Document Query Endpoint
# ==========================================
@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Embeds the incoming user query, searches Qdrant for matching 
    context chunks, and synthesizes an answer using the LLM.
    """
    try:
        result = await query_rag_pipeline(
            user_query=request.query, 
            top_k=request.top_k
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG pipeline: {str(e)}"
        )