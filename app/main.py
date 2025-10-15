from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.routes_chatbot import router as chatbot_router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A chatbot API for product inquiries using Groq LLM and LangGraph for task 2",
    version="1.0.0",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chatbot_router, prefix="/api", tags=["chatbot"])

@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to Product Chatbot REST API",
        "version": "1.0.0",
        "framework": "FastAPI with LangGraph",
        "llm": "Groq -"+settings.groq_model,
        "endpoints": {
            "get_products": "GET /api/products",
            "chat": "POST /api/chat",

        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )