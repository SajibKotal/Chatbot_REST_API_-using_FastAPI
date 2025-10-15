from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # Groq API Configuration
    groq_api_key: str = os.getenv("GOOGLE_GEMINI_API_KEY")
    groq_model: str = "llama-3.3-70b-versatile"
    # groq_model: str = "llama-3.1-8b-instant"
    
    # Dummy json API base_ulr
    dummyjson_base_url: str = "https://dummyjson.com"
    
    # Application Settings
    app_name: str = "Product Chatbot API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()