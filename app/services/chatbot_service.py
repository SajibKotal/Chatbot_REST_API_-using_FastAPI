import os
import json
from typing import List, Annotated, TypedDict, Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, AnyMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from utils.groq_client import groq_client
from utils.tool import cutomized_tool
from models.schemas import ProductSearchInput,HighRatedTitlesInput

# Define Tools
@tool("search_products_tool", args_schema=ProductSearchInput)
async def search_products_tool(query: str) -> dict:
    """Search for products by name, brand, or category."""
    try:
        products = await cutomized_tool.search_products(query)  # have used  DummyJSON API for to get relevent product details
        return products.model_dump()
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@tool("get_high_rated_titles_tool", args_schema=HighRatedTitlesInput)
async def get_high_rated_titles_tool(min_rating: float = 4.0) -> dict:
    """Get product titles with high ratings (above specified threshold). Returns only titles and ratings."""
    try:
        high_rated_titles = await cutomized_tool.get_high_rated_titles(min_rating)
                     
        return high_rated_titles.model_dump()
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
# List of all tools
PRODUCT_TOOLS = [
    search_products_tool,
    get_high_rated_titles_tool,
]

class ChatbotService:
    def __init__(self):
        self.tools = PRODUCT_TOOLS
        self.llm = groq_client.get_client()
        self.llm_with_tools = self.llm.bind_tools(self.tools)
    
    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process user message using LangGraph with tool calling"""
        try:
            # System prompt
            SYSTEM_PROMPT = """You are a smart Product Assistant chatbot for an e-commerce store.
            
            INSTRUCTIONS:
            - Assist customers with product inquiries in a friendly, helpful manner
            - Extract product names, categories, or brands from user queries. Extract rating if mentioned
            - Make sure you use the tools to get accurate product information.
            - Then call `search_products_tool` with the product name or brand, or call `get_high_rated_titles_tool` with rating
            - Give natural responses with product features, prices, category and ratings that you get from tool calling.
            - Be conversational but informative.
            - Always use tools to get real data before responding.
            
            Examples:
            User: "Tell me about iPhone 9" → Use search_products_tool with "iPhone 9"
            User: "Show me products with ratings above 4" → Use get_high_rated_titles_tool with min_rating=4.0
            User: "What are highly rated products?" → Use get_high_rated_titles_tool
            """
            
            # LangGraph state
            class AgentState(TypedDict):
                messages: Annotated[List[AnyMessage], add_messages]
            
            def call_model(state: AgentState):
                return {"messages": [self.llm_with_tools.invoke(state["messages"])]}
            
            def router(state: AgentState):
                last = state["messages"][-1]
                if isinstance(last, AIMessage) and last.tool_calls:
                    return "tools"
                return END
            
            # Build graph
            graph = StateGraph(AgentState)
            graph.add_node("agent", call_model)
            graph.add_node("tools", ToolNode(self.tools))
            graph.add_edge("tools", "agent")
            graph.add_conditional_edges("agent", router, {"tools": "tools", END: END})
            graph.set_entry_point("agent")
            
            app = graph.compile()
            

            # show the visualization image of the workflow
            image_data = app.get_graph().draw_mermaid_png()
            with open("workflow_visualization.png", "wb") as f:
                f.write(image_data)
                
            # Run the graph
            state = {"messages": [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=message)]}
            result = app.invoke(state)
            
            # Extract response and tool usage
            final_message = result["messages"][-1]
            
            response_data = {
                "response": final_message.content,

            }
            
            return response_data
            
        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}",

            }
    

# Global instance
chatbot_service = ChatbotService()