import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to hold environment variables and settings"""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    
    # Model Selection
    MODEL_NAME = "mistral-small-latest"
    VISION_MODEL_NAME = "pixtral-12b-2409"
    
    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
