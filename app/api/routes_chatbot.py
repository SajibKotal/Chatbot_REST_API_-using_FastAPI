from fastapi import APIRouter, HTTPException, status
from typing import List
from services.chatbot_service import chatbot_service, PRODUCT_TOOLS
from services.product_service import product_service
from models.schemas import (
    ChatRequest, 
    ChatResponse, 
    ProductsResponse,
    ErrorResponse
)

router = APIRouter()

@router.get(
    "/products",
    response_model=ProductsResponse,
    summary="Get all products",
    description="Fetch all product data from DummyJSON Products API",
    responses={
        200: {"model": ProductsResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_all_products():
    """
    Retrieve all products from the DummyJSON API
    """
    try:
        products = await product_service.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the product bot",
    description="Send a message to the chatbot and get a human-like response about products",
    responses={
        200: {"model": ChatResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def chat_with_bot(chat_request: ChatRequest):
    """
    Process customer message and provide intelligent response about products
    """
    if not chat_request.message or not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    try:
        result = await chatbot_service.process_message(chat_request.message.strip())
        
        return ChatResponse(
            response=result["response"],
            
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )





