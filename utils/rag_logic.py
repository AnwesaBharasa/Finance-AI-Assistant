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
KNOWLEDGE_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../knowledge_base"))
INDEXED_FILES_TRACKER = os.path.join(VECTOR_STORE_PATH, "indexed_files.txt")

def process_and_store_pdf(file_path: str, is_permanent: bool = False):
    """Load uploaded PDFs, chunk + embed text, store vector DB (persist locally)"""
    try:
        file_name = os.path.basename(file_path)
        logger.info(f"Processing PDF: {file_name}")
        
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
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
        vector_store.save_local(VECTOR_STORE_PATH)
        
        # Track indexed file
        with open(INDEXED_FILES_TRACKER, "a") as f:
            f.write(f"{file_name}\n")
            
        logger.info(f"Successfully persisted vector store for {file_name}.")
        return True, f"Successfully indexed {file_name}."
    except Exception as e:
        error_msg = f"Error processing {os.path.basename(file_path)}: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def sync_knowledge_base():
    """Sync all PDFs from knowledge_base directory into the vector store."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        return 0, "Created empty knowledge_base directory."
        
    # Get already indexed files
    indexed_files = set()
    if os.path.exists(INDEXED_FILES_TRACKER):
        with open(INDEXED_FILES_TRACKER, "r") as f:
            indexed_files = {line.strip() for line in f if line.strip()}
            
    files_to_sync = [f for f in os.listdir(KNOWLEDGE_BASE_DIR) if f.lower().endswith(".pdf") and f not in indexed_files]
    
    count = 0
    errors = []
    
    for file_name in files_to_sync:
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, file_name)
        success, msg = process_and_store_pdf(file_path, is_permanent=True)
        if success:
            count += 1
        else:
            errors.append(msg)
            
    if errors:
        return count, f"Synced {count} files. Errors: {'; '.join(errors)}"
    return count, f"Knowledge Base Synchronized: {count} new files added."

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
