import os
from agent.agent import ShopServiceAgent

def main():
    """
    Main entry point for the e-commerce customer service chatbot.
    Initializes the agent and handles the chat loop.
    """
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    
    # Initialize the customer services agent
    agent = ShopServiceAgent(api_key)
    
    # Start the chat loop
    print("AI Customer Service Assistant started. Please enter your question (type 'quit' to exit)")
    
    while True:
        # Get user input
        user_input = input("User: ")
        if user_input.lower() == 'quit':
            break
            
        try:
            # Process user input and get response
            response = agent.think(user_input)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 