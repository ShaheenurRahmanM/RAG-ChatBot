"""
Utility functions for RAG pipeline
"""
import os
from typing import List, Dict
import fitz  # PyMuPDF

def get_pdf_files(pdf_path: str) -> List[str]:
    """
    Get all PDF files from the specified directory
    
    Args:
        pdf_path: Path to directory containing PDFs
        
    Returns:
        List of absolute paths to PDF files
    """
    pdf_files = []
    if not os.path.exists(pdf_path):
        print(f"Warning: PDF directory does not exist: {pdf_path}")
        return pdf_files
    
    for file in os.listdir(pdf_path):
        if file.lower().endswith('.pdf'):
            full_path = os.path.join(pdf_path, file)
            pdf_files.append(full_path)
    
    return pdf_files


def extract_text_from_pdf(pdf_path: str) -> Dict[str, any]:
    """
    Extract text from PDF file using PyMuPDF
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dictionary with document name and pages with text and metadata
    """
    try:
        doc = fitz.open(pdf_path)
        pdf_name = os.path.basename(pdf_path)
        pages = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            pages.append({
                "text": text,
                "page_number": page_num + 1,
                "source": pdf_name
            })
        
        doc.close()
        return {
            "name": pdf_name,
            "pages": pages
        }
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return None


def format_sources(sources: List[str]) -> List[str]:
    """
    Format source documents by removing duplicates and sorting
    
    Args:
        sources: List of source document names
        
    Returns:
        Formatted list of unique sources
    """
    return sorted(list(set(sources)))


def ensure_directory_exists(path: str) -> None:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        path: Directory path to ensure exists
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")
