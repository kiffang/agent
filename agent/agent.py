from typing import List, Dict
import openai 
import json
from .database import ShopDatabase
from .rl_optimizer import RLOptimizer

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
        self.rl_optimizer = RLOptimizer()  # Initialize RL optimizer
        
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
        
        # Get current state from conversation history
        current_state = self.rl_optimizer.get_state_features(self.conversation_history)
        
        # Get best response type based on learned Q-values
        best_response_type = self.rl_optimizer.get_best_response_type(current_state)
        
        # Modify system prompt based on learned response type
        system_prompt = self._get_optimized_prompt(best_response_type)
        
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
        
        # Prepare messages for API call
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history
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
        
        # Extract features from response
        action = self.rl_optimizer.get_action_features(assistant_response)
        
        # Store state and action for later update
        self.rl_optimizer.state_history.append(current_state)
        self.rl_optimizer.action_history.append(action)
        
        return assistant_response
        
    def _get_optimized_prompt(self, response_type: str) -> str:
        """
        Generate optimized system prompt based on learned response type.
        """
        base_prompt = """You are a professional e-commerce customer service assistant. You should:
        1. Use polite and professional language, address users as "dear"
        2. Keep responses concise and clear
        3. When uncertain, apologize and suggest consulting human customer service
        4. Handle orders, logistics, returns, and exchanges
        5. Recommend products based on user needs
        6. Provide accurate price information
        7. Proactively ask if users need anything else
        """
        
        # Customize prompt based on response types
        if "brief" in response_type:
            base_prompt += "\nFocus on providing brief, direct answers."
        elif "detailed" in response_type:
            base_prompt += "\nProvide detailed explanations and additional helpful information."
            
        if "price_info" in response_type:
            base_prompt += "\nEmphasize pricing details and available discounts."
        elif "order_info" in response_type:
            base_prompt += "\nFocus on order status and delivery information."
            
        return base_prompt
        
    def provide_feedback(self, user_feedback: str):
        """
        Process user feedback and update RL model.
        """
        if not self.rl_optimizer.state_history:
            return
            
        # Calculate reward based on feedback
        reward = self.rl_optimizer.get_reward(user_feedback)
        
        # Get current state and action
        state = self.rl_optimizer.state_history[-1]
        action = self.rl_optimizer.action_history[-1]
        
        # Get next state
        next_state = self.rl_optimizer.get_state_features(self.conversation_history)
        
        # Update Q-values
        self.rl_optimizer.update(state, action, reward, next_state)