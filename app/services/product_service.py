import httpx
from typing import List, Optional, Dict, Any
from models.schemas import Product, ProductsResponse
from core.config import settings
import json
class ProductService:
    def __init__(self):
        self.base_url = settings.dummyjson_base_url
    
    async def get_all_products(self) -> ProductsResponse:
        """Fetch all products from DummyJSON API with proper error handling"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/products?limit=0",   # limit 0 means all product will shows
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Validate and clean each product
                validated_products = []
                for product_data in data.get("products", []):
                    try:
                        # Ensure all required fields have defaults
                        cleaned_product = {
                            "id": product_data.get("id", 0),
                            "title": product_data.get("title", "Unknown Product"),
                            "description": product_data.get("description", "No description available"),
                            "price": product_data.get("price", 0.0),
                            "discountPercentage": product_data.get("discountPercentage", 0.0),
                            "rating": product_data.get("rating", 0.0),
                            "stock": product_data.get("stock", 0),
                            "brand": product_data.get("brand", "Unknown Brand"),
                            "category": product_data.get("category", "uncategorized"),
                            "thumbnail": product_data.get("thumbnail", ""),
                            "images": product_data.get("images", [])
                        }
                        validated_products.append(Product(**cleaned_product))
                    except Exception as e:
                        print(f"Skipping invalid product {product_data.get('id')}: {e}")
                        continue
                
                return ProductsResponse(
                    products=validated_products,
                    total=data.get("total", len(validated_products)),
                    skip=data.get("skip", 0),
                    limit=data.get("limit", len(validated_products))
                )
                
            except httpx.HTTPError as e:
                raise Exception(f"Failed to fetch products: {str(e)}")
            except json.JSONDecodeError as e:
                raise Exception(f"Invalid JSON response: {str(e)}")
    

    
    
    
 

# Global instance
product_service = ProductService()