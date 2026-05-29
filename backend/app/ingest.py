"""
Document ingestion pipeline for PDF processing and embedding generation
"""
import sys
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    PDF_DATA_PATH
)
from utils import get_pdf_files, extract_text_from_pdf, ensure_directory_exists


def create_documents_from_pdfs() -> List[Document]:
    """
    Load PDFs and create LangChain Document objects
    
    Returns:
        List of LangChain Document objects
    """
    print("=" * 60)
    print("STARTING PDF INGESTION PIPELINE")
    print("=" * 60)
    
    documents = []
    pdf_files = get_pdf_files(PDF_DATA_PATH)
    
    if not pdf_files:
        print(f"No PDF files found in {PDF_DATA_PATH}")
        print("Please add PDF files to the data/pdfs/ directory")
        return documents
    
    print(f"\nFound {len(pdf_files)} PDF file(s)")
    print("-" * 60)
    
    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path}")
        pdf_data = extract_text_from_pdf(pdf_path)
        
        if pdf_data is None:
            continue
        
        pdf_name = pdf_data["name"]
        pages = pdf_data["pages"]
        print(f"  - Extracted {len(pages)} page(s)")
        
        # Create Document objects for each page
        for page in pages:
            doc = Document(
                page_content=page["text"],
                metadata={
                    "source": pdf_name,
                    "page": page["page_number"],
                    "chunk_index": 0  # Will be updated during chunking
                }
            )
            documents.append(doc)
    
    print(f"\nTotal pages extracted: {len(documents)}")
    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks using RecursiveCharacterTextSplitter
    
    Args:
        documents: List of Document objects
        
    Returns:
        List of split Document objects
    """
    print("\n" + "=" * 60)
    print("SPLITTING DOCUMENTS INTO CHUNKS")
    print("=" * 60)
    print(f"Chunk size: {CHUNK_SIZE}")
    print(f"Chunk overlap: {CHUNK_OVERLAP}")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    split_docs = splitter.split_documents(documents)
    print(f"\nTotal chunks created: {len(split_docs)}")
    
    # Update chunk_index in metadata
    for idx, doc in enumerate(split_docs):
        doc.metadata["chunk_index"] = idx
    
    return split_docs


def create_embeddings_and_store():
    """
    Main function to orchestrate the entire ingestion pipeline:
    1. Load PDFs
    2. Split documents
    3. Generate embeddings
    4. Store in ChromaDB
    """
    try:
        # Step 1: Ensure ChromaDB directory exists
        ensure_directory_exists(CHROMA_DB_PATH)
        
        # Step 2: Create documents from PDFs
        documents = create_documents_from_pdfs()
        
        if not documents:
            print("\nNo documents to process. Exiting.")
            return False
        
        # Step 3: Split documents into chunks
        split_docs = split_documents(documents)
        
        # Step 4: Initialize embeddings
        print("\n" + "=" * 60)
        print("INITIALIZING EMBEDDING MODEL")
        print("=" * 60)
        print(f"Model: {EMBEDDING_MODEL}")
        print("Downloading model... (this may take a moment on first run)")
        
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )
        print("✓ Embedding model loaded successfully")
        
        # Step 5: Create ChromaDB vector store
        print("\n" + "=" * 60)
        print("STORING EMBEDDINGS IN CHROMADB")
        print("=" * 60)
        print(f"ChromaDB path: {CHROMA_DB_PATH}")
        print(f"Collection name: {CHROMA_COLLECTION_NAME}")
        
        # Create vector store from documents
        vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            collection_name=CHROMA_COLLECTION_NAME,
            persist_directory=CHROMA_DB_PATH
        )
        
        print(f"✓ Successfully stored {len(split_docs)} chunks in ChromaDB")
        
        # Step 6: Print summary
        print("\n" + "=" * 60)
        print("INGESTION PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Total documents processed: {len(documents)}")
        print(f"Total chunks created: {len(split_docs)}")
        print(f"Vector store persisted at: {CHROMA_DB_PATH}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = create_embeddings_and_store()
    sys.exit(0 if success else 1)
