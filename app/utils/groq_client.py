from langchain_groq import ChatGroq
from core.config import settings

class GroqClient:
    def __init__(self):
        self.client = ChatGroq(
            groq_api_key=settings.groq_api_key,
            model_name=settings.groq_model,
            temperature=0.1
        )
    
    def get_client(self):
        return self.client

# Global instance
groq_client = GroqClient()