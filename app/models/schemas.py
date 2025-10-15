from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Product Models with optional fields to handle API inconsistencies
class Product(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float = Field(default=0.0)
    rating: float = Field(default=0.0, ge=0, le=5)
    stock: int = Field(default=0)
    brand: str 
    # warrantyInformation= str
    # shippingInformation=str
    # availabilityStatus=str
    


class ProductsResponse(BaseModel):
    products: List[Product]
    total: int
    skip: int
    limit: int

# Chat Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# Error Models
class ErrorResponse(BaseModel):
    detail: str

# Tool Models
class ProductSearchInput(BaseModel):
    query: str = Field(description="Product name, brand, or category to search for")


class PriceComparisonInput(BaseModel):
    product_names: List[str] = Field(description="List of product names to compare")

class HighRatedTitlesInput(BaseModel):
    min_rating: float = Field(default=4.0, description="Minimum rating threshold", ge=0, le=5)
class HighRatedTitlesOutput(BaseModel):
    product_title: List[str]