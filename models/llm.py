import os
import sys
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.config import Config

def get_chatgroq_model():
    """Initialize and return the Mistral AI LLM (function name kept for compatibility)"""
    try:
        llm = ChatMistralAI(
            api_key=Config.MISTRAL_API_KEY,
            model=Config.MODEL_NAME,
            temperature=0,
        )
        return llm
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Mistral model: {str(e)}")

def get_vision_response(image_base64: str, query: str, system_prompt: str):
    """Vision analysis using Mistral Pixtral model."""
    try:
        if not Config.MISTRAL_API_KEY:
            return "MISTRAL_API_KEY is missing! Please add it to your `.env` file."
            
        vision_llm = ChatMistralAI(
            api_key=Config.MISTRAL_API_KEY,
            model=Config.VISION_MODEL_NAME,
            temperature=0,
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(
                content=[
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ]
            )
        ]
        
        response = vision_llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"