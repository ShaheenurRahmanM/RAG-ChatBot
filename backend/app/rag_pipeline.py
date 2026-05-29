"""
RAG (Retrieval-Augmented Generation) Pipeline using LangChain
"""
from typing import Dict, List, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

try:
    # Try newer import path first
    from langchain.chains import create_retrieval_chain, create_stuff_documents_chain
except ImportError:
    # Fall back to older import path
    from langchain.chains.retrieval import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain

try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    # Fall back to older import path
    from langchain.prompts import ChatPromptTemplate

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    RETRIEVER_K
)
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from utils import format_sources, ensure_directory_exists


class RAGPipeline:
    """
    Retrieval-Augmented Generation Pipeline using LangChain
    """
    
    def __init__(self):
        """Initialize the RAG pipeline with embeddings, vector store, and LLM"""
        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self.llm = None
        self.chain = None
        self._initialize()
    
    def _initialize(self):
        """Initialize all components of the RAG pipeline"""
        try:
            print("Initializing RAG Pipeline...")
            
            # Initialize embeddings
            print("  - Loading embedding model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={"device": "cpu"}
            )
            
            # Initialize ChromaDB vector store
            print("  - Connecting to ChromaDB...")
            self.vector_store = Chroma(
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=CHROMA_DB_PATH
            )
            
            # Create retriever with similarity search
            print("  - Setting up retriever...")
            self.retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": RETRIEVER_K}
            )
            
            # Initialize Groq LLM
            print("  - Initializing Groq LLM...")
            self.llm = ChatGroq(
                groq_api_key=GROQ_API_KEY,
                model_name=GROQ_MODEL,
                temperature=0.3,  # Lower temperature for more consistent answers
                top_p=0.9
            )
            
            # Create retrieval chain
            print("  - Setting up retrieval chain...")
            self._create_chain()
            
            print("✓ RAG Pipeline initialized successfully\n")
            
        except Exception as e:
            print(f"❌ Error initializing RAG Pipeline: {str(e)}")
            raise
    
    def _create_chain(self):
        """Create the LangChain retrieval chain"""
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", USER_PROMPT_TEMPLATE)
        ])
        
        # Create the combine documents chain
        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        
        # Create the retrieval chain
        self.chain = create_retrieval_chain(self.retriever, combine_docs_chain)
    
    def query(self, question: str) -> Tuple[str, List[str]]:
        """
        Process a user question and generate a grounded response
        
        Args:
            question: User's question
            
        Returns:
            Tuple of (answer, sources)
        """
        try:
            # Run the retrieval chain
            result = self.chain.invoke({"input": question})
            
            # Extract answer
            answer = result.get("answer", "I don't have that information in the company documents.")
            
            # Extract sources from context
            context_docs = result.get("context", [])
            sources = []
            
            for doc in context_docs:
                source = doc.metadata.get("source", "Unknown")
                if source not in sources:
                    sources.append(source)
            
            sources = format_sources(sources)
            
            return answer, sources
            
        except Exception as e:
            print(f"Error during query: {str(e)}")
            return f"Error processing query: {str(e)}", []
    
    def is_ready(self) -> bool:
        """
        Check if the RAG pipeline is ready to answer questions
        
        Returns:
            Boolean indicating if pipeline is initialized and ready
        """
        return (
            self.embeddings is not None and
            self.vector_store is not None and
            self.retriever is not None and
            self.llm is not None and
            self.chain is not None
        )
    
    def get_vector_store_info(self) -> Dict:
        """
        Get information about the vector store
        
        Returns:
            Dictionary with vector store information
        """
        try:
            if self.vector_store is None:
                return {"error": "Vector store not initialized"}
            
            # Try to get collection info
            collection = self.vector_store._collection
            doc_count = collection.count()
            
            return {
                "collection_name": CHROMA_COLLECTION_NAME,
                "document_count": doc_count,
                "embedding_model": EMBEDDING_MODEL,
                "retriever_k": RETRIEVER_K,
                "chunk_size": 500,
                "chunk_overlap": 50
            }
        except Exception as e:
            return {
                "error": f"Could not retrieve vector store info: {str(e)}"
            }


# Global RAG pipeline instance
_rag_pipeline = None


def get_rag_pipeline() -> RAGPipeline:
    """
    Get or create the global RAG pipeline instance
    
    Returns:
        RAGPipeline instance
    """
    global _rag_pipeline
    
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    
    return _rag_pipeline
