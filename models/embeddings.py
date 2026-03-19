from langchain_community.embeddings import HuggingFaceEmbeddings
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import Config

def get_embeddings_model():
    """Initialize and return the HuggingFace embeddings model securely"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL
        )
        return embeddings
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embeddings model: {str(e)}")
