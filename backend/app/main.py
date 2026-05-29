"""
FastAPI application for SWS AI Policy Assistant
Main application with RAG-powered chat endpoints
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from config import CORS_ORIGINS
from rag_pipeline import get_rag_pipeline

# Initialize FastAPI app
app = FastAPI(
    title="SWS AI Policy Assistant",
    description="RAG-powered chatbot for company policy documents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    sources: List[str]


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    message: str = "RAG pipeline is ready"


class InfoResponse(BaseModel):
    """Response model for info endpoint"""
    status: str
    pipeline_ready: bool
    vector_store_info: dict = None


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "SWS AI Policy Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Health status of the application
    """
    try:
        rag_pipeline = get_rag_pipeline()
        
        if rag_pipeline.is_ready():
            vector_store_info = rag_pipeline.get_vector_store_info()
            doc_count = vector_store_info.get("document_count", 0)
            
            if doc_count == 0:
                return HealthResponse(
                    status="warning",
                message="RAG pipeline is ready but no documents have been ingested. Please run: py app/ingest.py"
            return HealthResponse(
                status="ok",
                message=f"RAG pipeline is ready with {doc_count} document chunks"
            )
        else:
            return HealthResponse(
                status="error",
                message="RAG pipeline is not properly initialized"
            )
    except Exception as e:
        return HealthResponse(
            status="error",
            message=f"Error checking health: {str(e)}"
        )


@app.get("/api/info", response_model=InfoResponse, tags=["Info"])
async def info():
    """
    Get information about the RAG pipeline
    
    Returns:
        Information about pipeline configuration and status
    """
    try:
        rag_pipeline = get_rag_pipeline()
        vector_store_info = rag_pipeline.get_vector_store_info()
        
        return InfoResponse(
            status="ok",
            pipeline_ready=rag_pipeline.is_ready(),
            vector_store_info=vector_store_info
        )
    except Exception as e:
        return InfoResponse(
            status="error",
            pipeline_ready=False,
            vector_store_info={"error": str(e)}
        )


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint for RAG-powered responses
    
    Args:
        request: ChatRequest containing the user's question
        
    Returns:
        ChatResponse with answer and sources
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        # Validate input
        if not request.question or request.question.strip() == "":
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        question = request.question.strip()
        
        # Get RAG pipeline
        rag_pipeline = get_rag_pipeline()
        
        # Check if pipeline is ready
        if not rag_pipeline.is_ready():
            raise HTTPException(
                status_code=503,
                detail="RAG pipeline is not initialized. Please ingest documents first: py app/ingest.py"
            )
        
        # Check if vector store has documents
        vector_store_info = rag_pipeline.get_vector_store_info()
        if vector_store_info.get("document_count", 0) == 0:
            raise HTTPException(
                status_code=503,
                detail="No documents have been ingested. Please add PDFs to data/pdfs/ and run: py app/ingest.py"
            )
        
        # Query the RAG pipeline
        answer, sources = rag_pipeline.query(question)
        
        return ChatResponse(
            answer=answer,
            sources=sources
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on application startup"""
    print("\n" + "=" * 60)
    print("SWS AI POLICY ASSISTANT - STARTING UP")
    print("=" * 60)
    
    try:
        rag_pipeline = get_rag_pipeline()
        print("✓ Application started successfully")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"❌ Error during startup: {str(e)}")
        print("Make sure to run: python app/ingest.py")
        print("=" * 60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("\n" + "=" * 60)
    print("SWS AI POLICY ASSISTANT - SHUTTING DOWN")
    print("=" * 60 + "\n")


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    print(f"Unhandled exception: {str(exc)}")
    return {
        "error": "Internal server error",
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT, API_RELOAD
    
    print("\n" + "=" * 60)
    print("Starting SWS AI Policy Assistant API")
    print(f"Host: {API_HOST}:{API_PORT}")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD
    )
