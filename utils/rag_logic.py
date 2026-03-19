import os
import sys
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.embeddings import get_embeddings_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

def process_and_store_pdf(file_path: str):
    """Load uploaded PDFs, chunk + embed text, store vector DB (persist locally)"""
    try:
        logger.info(f"Processing PDF: {file_path}")
        # Load PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        # Chunk text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        
        # Embed and store
        embeddings = get_embeddings_model()
        
        # Check if vector DB already exists locally
        if os.path.exists(VECTOR_STORE_PATH):
            logger.info("Updating existing FAISS vector store.")
            vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
            vector_store.add_documents(chunks)
        else:
            logger.info("Creating new FAISS vector store.")
            vector_store = FAISS.from_documents(chunks, embeddings)
            
        # Persist locally
        vector_store.save_local(VECTOR_STORE_PATH)
        logger.info("Successfully persisted vector store.")
        return True, "Successfully processed and stored PDF."
    except Exception as e:
        error_msg = f"Error processing PDF: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

class RagSearchInput(BaseModel):
    query: str = Field(description="The specific search query to look up in the uploaded financial documents.")

def rag_search(query: str) -> str:
    """Retrieve relevant chunks from the persisted FAISS vector DB."""
    try:
        if not os.path.exists(VECTOR_STORE_PATH):
            logger.info("No vector store found.")
            return "This is outside my document knowledge. (No document uploaded)"
            
        embeddings = get_embeddings_model()
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        
        docs = vector_store.similarity_search(query, k=3)
        
        if docs:
            context = "\n\n".join([doc.page_content for doc in docs])
            logger.info(f"Retrieved {len(docs)} documents for query.")
            return context
        return "This is outside my document knowledge."
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        return f"This is outside my document knowledge. (Error: {str(e)})"

def rag_search_tool():
    """Create and return a LangChain Tool for Document Search"""
    return StructuredTool.from_function(
        func=rag_search,
        name="document_search",
        description="Search strictly within the uploaded financial or tax documents (PDFs) for exact context. Use this for ANY domain-specific query. If the query is outside the document domain, the tool will explicitly state 'This is outside my document knowledge'.",
        args_schema=RagSearchInput
    )
