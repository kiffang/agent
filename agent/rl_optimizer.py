import numpy as np
from typing import List, Dict
from collections import defaultdict

class RLOptimizer:
    """
    Reinforcement Learning optimizer for customer service responses.
    Uses Q-learning to optimize response strategies based on customer feedback.
    """
    def __init__(self, learning_rate=0.1, discount_factor=0.95):
        self.learning_rate = learning_rate  # Learning rate for Q-learning
        self.discount_factor = discount_factor  # Discount factor for future rewards
        self.q_table = defaultdict(lambda: defaultdict(float))  # Q-table for storing state-action values
        self.state_history = []  # Store conversation states
        self.action_history = []  # Store taken actions
        
    def get_state_features(self, conversation_history: List[Dict]) -> str:
        """
        Extract relevant features from conversation history to create state representation.
        
        Args:
            conversation_history: List of conversation messages
            
        Returns:
            str: State representation
        """
        if not conversation_history:
            return "initial_state"
            
        # Extract last user message
        last_user_msg = None
        for msg in reversed(conversation_history):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break
                
        # Simple state features (can be expanded)
        features = []
        
        # Message length feature
        if last_user_msg:
            if len(last_user_msg) < 10:
                features.append("short_query")
            elif len(last_user_msg) < 30:
                features.append("medium_query")
            else:
                features.append("long_query")
                
        # Query type features
        query_types = {
            "price": ["price", "cost", "how much"],
            "product": ["specs", "features", "details"],
            "order": ["order", "tracking", "delivery"],
            "complaint": ["problem", "issue", "wrong", "bad"]
        }
        
        if last_user_msg:
            last_user_msg = last_user_msg.lower()
            for qtype, keywords in query_types.items():
                if any(keyword in last_user_msg for keyword in keywords):
                    features.append(qtype)
                    
        return "_".join(features) if features else "general_query"
    
    def get_action_features(self, response: str) -> str:
        """
        Extract features from agent's response to create action representation.
        
        Args:
            response: Agent's response text
            
        Returns:
            str: Action representation
        """
        features = []
        
        # Response length feature
        if len(response) < 50:
            features.append("brief")
        elif len(response) < 150:
            features.append("moderate")
        else:
            features.append("detailed")
            
        # Response type features
        if "price" in response.lower():
            features.append("price_info")
        if "order" in response.lower():
            features.append("order_info")
        if "sorry" in response.lower() or "apologize" in response.lower():
            features.append("apology")
        if "?" in response:
            features.append("question")
            
        return "_".join(features)
    
    def get_reward(self, user_feedback: str) -> float:
        """
        Calculate reward based on user feedback or response.
        
        Args:
            user_feedback: User's next message or explicit feedback
            
        Returns:
            float: Reward value
        """
        # Positive feedback indicators
        positive_words = ["thanks", "thank you", "helpful", "good", "great", "perfect"]
        # Negative feedback indicators
        negative_words = ["not helpful", "bad", "wrong", "incorrect", "confused"]
        
        user_feedback = user_feedback.lower()
        
        # Calculate reward
        reward = 0.0
        
        # Check for positive feedback
        if any(word in user_feedback for word in positive_words):
            reward += 1.0
            
        # Check for negative feedback
        if any(word in user_feedback for word in negative_words):
            reward -= 1.0
            
        # Length-based penalties to encourage concise responses
        if len(user_feedback) > 200:  # If user needs to write a long response, might indicate unclear answer
            reward -= 0.2
            
        return reward
    
    def update(self, state: str, action: str, reward: float, next_state: str):
        """
        Update Q-values based on received reward.
        
        Args:
            state: Current state
            action: Taken action
            reward: Received reward
            next_state: Resulting state
        """
        # Get current Q-value
        current_q = self.q_table[state][action]
        
        # Get maximum Q-value for next state
        next_max_q = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        
        # Q-learning update formula
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - current_q
        )
        
        # Update Q-table
        self.q_table[state][action] = new_q
    
    def get_best_response_type(self, state: str) -> str:
        """
        Get the best response type for current state based on Q-values.
        
        Args:
            state: Current conversation state
            
        Returns:
            str: Best response type
        """
        if not self.q_table[state]:
            return "moderate_general"  # Default response type
            
        return max(self.q_table[state].items(), key=lambda x: x[1])[0] 