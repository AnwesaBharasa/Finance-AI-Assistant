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
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
    DEMO_USERNAME = os.getenv("DEMO_USERNAME", "demo")
    DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "demo123")
    
    # Model Selection
    MODEL_NAME = "mistral-small-latest"
    VISION_MODEL_NAME = "pixtral-12b-2409"
    
    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
