import httpx
from typing import List, Optional, Dict, Any
from models.schemas import Product, ProductsResponse,HighRatedTitlesOutput
from core.config import settings
import json
class CustomizedTool:
    def __init__(self):
        self.base_url = settings.dummyjson_base_url
    async def search_products(self, query: str) -> Product:
            """Search products by query"""
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        f"{self.base_url}/products/search?q={query}",
                        timeout=30.0
                    )
                    if response.status_code == 200:

                        response.raise_for_status()
                        data = response.json()
                        
                    
                        return Product(
                            
                            id=data["id"], 
                            title=data["title"],
                            description=data["description"],
                            price= data["price"],
                            discountPercentage= data["discountPercentage"],
                            rating= data["rating"], 
                            stock= data["stock"],
                            brand= data["brand"], 
                            category= data["category"], 
                            # warrantyInformation=["warrantyInformation"],
                            # shippingInformation=["shippingInformation"],
                            # availabilityStatus=["availabilityStatus"],
                            )
                    else:
                        raise ValueError(f"product {query} not found")
                    
                except httpx.HTTPError as e:
                    raise Exception(f"Failed to search products: {str(e)}")

    async def get_high_rated_titles(self, min_rating: float = 4.0) -> List[Dict[str, Any]]:
        """Get only product titles with rating above specified threshold"""
        async with httpx.AsyncClient() as client:
            try:
                # Use the optimized API endpoint that only returns title and rating from dummyjson
                response = await client.get(
                    f"{self.base_url}/products?limit=0&select=title,rating",
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # Filter products by rating and extract only titles
                high_rated_titles = [
                    {
                        "title": product.get("title", "Unknown Product"),
                        "rating": product.get("rating", 0.0)
                    }
                    for product in data.get("products", [])
                    if product.get("rating", 0) >= min_rating
                ]
                
                # Sort by rating (descending)
                high_rated_titles.sort(key=lambda x: x["rating"], reverse=True)
                # Extract just the titles for the main response
                titles_only = [item["title"] for item in high_rated_titles]                
                return HighRatedTitlesOutput(titles_only)
                
            except httpx.HTTPError as e:
                raise Exception(f"Failed to fetch high-rated titles: {str(e)}")    


# Global instance
cutomized_tool = CustomizedTool()