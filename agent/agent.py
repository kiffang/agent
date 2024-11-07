from typing import List, Dict
import openai
import json
from .database import ShopDatabase

class ShopServiceAgent:
    """
    A customer service agent for e-commerce platform.
    Handles user queries about products, orders, and logistics using OpenAI's GPT model.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the agent with OpenAI API key and setup the database connection.
        
        Args:
            api_key (str): OpenAI API key for authentication
        """
        self.api_key = api_key
        openai.api_key = api_key
        self.conversation_history = []  # Stores the conversation context
        self.db = ShopDatabase()  # Initialize database connection
        
    def get_product_info(self, product_name: str) -> Dict:
        """
        Get product information from database.
        
        Args:
            product_name (str): Name of the product to query
            
        Returns:
            Dict: Product information including price, stock, specs, etc.
        """
        return self.db.get_product_info(product_name)
    
    def get_order_info(self, order_id: str) -> Dict:
        """
        Get order information from database.
        
        Args:
            order_id (str): Order ID to query
            
        Returns:
            Dict: Order information including status, tracking number, etc.
        """
        return self.db.get_order_info(order_id)
    
    def get_logistics_info(self, tracking_number: str) -> List:
        """
        Get logistics tracking information.
        
        Args:
            tracking_number (str): Shipping tracking number
            
        Returns:
            List: List of logistics status updates
        """
        return self.db.get_logistics_info(tracking_number)
    
    def search_products(self, category: str = None, price_range: tuple = None) -> List[Dict]:
        """
        Search products by category and price range.
        
        Args:
            category (str, optional): Product category to filter
            price_range (tuple, optional): Price range tuple (min_price, max_price)
            
        Returns:
            List[Dict]: List of matching products
        """
        return self.db.search_products(category, price_range)

    def think(self, user_input: str) -> str:
        """
        Process user input and generate appropriate response using GPT model.
        
        Args:
            user_input (str): User's question or command
            
        Returns:
            str: Assistant's response
        """
        # Add user input to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Define system prompt for the assistant's behavior
        system_prompt = """You are a professional e-commerce customer service assistant. You should:
        1. Use polite and professional language, address users as "dear"
        2. Keep responses concise and clear
        3. When uncertain, apologize and suggest consulting human customer service
        4. Handle orders, logistics, returns, and exchanges
        5. Recommend products based on user needs
        6. Provide accurate price information
        7. Proactively ask if users need anything else
        
        Available functions:
        - get_product_info(product_name): Get detailed product information
        - get_order_info(order_id): Get order information
        - get_logistics_info(tracking_number): Get logistics information
        - search_products(category, price_range): Search products by category and price range
        """
        
        # Prepare messages for API call
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history
        ]
        
        # Define available functions for the model
        functions = [
            {
                "name": "get_product_info",
                "description": "Get detailed product information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {"type": "string", "description": "Product name"}
                    },
                    "required": ["product_name"]
                }
            },
            {
                "name": "get_order_info",
                "description": "Get order information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "Order ID"}
                    },
                    "required": ["order_id"]
                }
            },
            {
                "name": "get_logistics_info",
                "description": "Get logistics information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tracking_number": {"type": "string", "description": "Tracking number"}
                    },
                    "required": ["tracking_number"]
                }
            },
            {
                "name": "search_products",
                "description": "Search products",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "description": "Product category"},
                        "price_range": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Price range [min_price, max_price]"
                        }
                    }
                }
            }
        ]
        
        # Make initial API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        
        response_message = response.choices[0].message
        
        # Handle function calls if any
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            function_args = json.loads(response_message["function_call"]["arguments"])
            
            # Map function names to actual functions
            function_mapping = {
                "get_product_info": self.get_product_info,
                "get_order_info": self.get_order_info,
                "get_logistics_info": self.get_logistics_info,
                "search_products": self.search_products
            }
            
            # Execute the function
            function_response = function_mapping[function_name](**function_args)
            
            # Add function response to conversation history
            self.conversation_history.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response, ensure_ascii=False)
            })
            
            # Make second API call with function response
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages + [
                    response_message,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(function_response, ensure_ascii=False)
                    }
                ]
            )
            assistant_response = second_response.choices[0].message.content
            
        else:
            assistant_response = response_message.content
            
        # Add assistant's response to conversation history
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response