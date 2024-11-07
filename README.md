# E-commerce Customer Service AI Agent

An intelligent customer service chatbot for e-commerce platforms, powered by OpenAI's GPT model and optimized with Reinforcement Learning. This assistant can handle product inquiries, order tracking, and general customer service tasks while continuously learning from user interactions.

## Features

- 🧠 **Reinforcement Learning Optimization**
  - Q-learning based response optimization
  - Adaptive conversation strategies
  - Continuous learning from user feedback
  - State-action value tracking

- 🛍️ **Product Information**
  - Search products by category and price range
  - Get detailed product specifications
  - Check product availability and pricing
  - View product reviews and ratings

- 📦 **Order Management**
  - Track order status
  - View order details
  - Check shipping information
  - Handle order inquiries

- 🚚 **Logistics Tracking**
  - Real-time shipping status updates
  - Delivery time estimates
  - Package location tracking

- 🛒 **Shopping Cart**
  - View cart contents
  - Add items to cart
  - Manage cart items

- 🎫 **Coupon Management**
  - Check available coupons
  - Verify coupon validity
  - View coupon conditions

## Installation

1. Clone the repository
2. Install the required packages
```bash
pip install -r requirements.txt
```
3. Set the OpenAI API key in the `.env` file  
```bash
OPENAI_API_KEY=<your_openai_api_key>
```

## Project Structure

```
ecommerce-ai-assistant/
├── agent/
│   ├── __init__.py
│   ├── agent.py        # Main agent logic
│   ├── database.py     # Mock database and data operations
│   └── rl_optimizer.py # Reinforcement learning optimization
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## RL System Details

### State Features
- Message length (short/medium/long query)
- Query type (price/product/order/complaint)
- Conversation context

### Action Features
- Response length (brief/moderate/detailed)
- Response type (price_info/order_info)
- Special actions (apology/question)

### Reward System
- Positive feedback: +1.0
- Negative feedback: -1.0
- Length penalties for unclear responses
- Continuous feedback learning

### Q-Learning Parameters
- Learning rate: 0.1
- Discount factor: 0.95
- Exploration vs exploitation balance

## Usage Examples

```python
# Initialize the agent
agent = ShopServiceAgent(api_key)

# Regular interaction
response = agent.think("What's the price of iPhone 15?")

# Provide feedback for RL optimization
agent.provide_feedback("Thanks, that was helpful!")
```

Example conversations:
```
User: What's the price of iPhone 15?
Assistant: The iPhone 15 is priced at $5,999. It comes in three storage options: 
128GB, 256GB, and 512GB. Would you like to know about any specific variant?

User: Show me phones between 5000 and 7000
Assistant: Here are the phones in that price range:
1. iPhone 15 ($5,999) - Latest A16 chip, great camera
2. Huawei Mate60 ($6,999) - Flagship with Kirin chip

User: Track my order ORDER2024030001
Assistant: Your order has been shipped via SF Express (tracking: SF1234567890). 
Current status: Out for delivery in Chaoyang District.
```
