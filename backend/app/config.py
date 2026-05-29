# """
# Configuration module for RAG pipeline
# """
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Groq API Configuration
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = "llama-3.1-8b-instant"

# # ChromaDB Configuration
# CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
# CHROMA_COLLECTION_NAME = "sws_documents"

# # PDF Configuration
# PDF_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "pdfs")

# # Chunking Configuration
# CHUNK_SIZE = 500
# CHUNK_OVERLAP = 50

# # Retrieval Configuration
# RETRIEVER_K = 4

# # Embedding Model
# EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# # CORS Configuration
# CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "*"]

# # API Configuration
# API_HOST = "0.0.0.0"
# API_PORT = 8000
# API_RELOAD = True


"""
Configuration module for RAG pipeline
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"   # updated: llama3-8b-8192 was decommissioned

# ChromaDB Configuration
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
CHROMA_COLLECTION_NAME = "sws_documents"

# PDF Configuration
PDF_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "pdfs")

# Chunking Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retrieval Configuration
# Raised from 4 → 8 so the LLM receives chunks from multiple PDFs per query.
# With k=4 and several PDFs, all 4 chunks often came from a single document.
RETRIEVER_K = 8

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# CORS Configuration
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "*"]

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True