import os
import sys
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

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

def retrieve_context(query: str, k: int = 3) -> str:
    """Retrieve relevant chunks from the persisted FAISS vector DB."""
    try:
        if not os.path.exists(VECTOR_STORE_PATH):
            logger.info("No vector store found.")
            return ""
            
        embeddings = get_embeddings_model()
        vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        
        docs = vector_store.similarity_search(query, k=k)
        
        if docs:
            context = "\n\n".join([doc.page_content for doc in docs])
            logger.info(f"Retrieved {len(docs)} documents for query.")
            return context
        return ""
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        return ""
