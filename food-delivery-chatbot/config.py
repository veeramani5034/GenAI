"""
Configuration for Food Delivery Chatbot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Settings
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('MODEL', 'gpt-4')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))

# Bot Settings
BOT_NAME = os.getenv('BOT_NAME', 'FoodBot')
COMPANY_NAME = os.getenv('COMPANY_NAME', 'QuickBite')

# Business Settings
DEFAULT_DELIVERY_TIME = int(os.getenv('DEFAULT_DELIVERY_TIME', '30'))
REFUND_PROCESSING_DAYS = int(os.getenv('REFUND_PROCESSING_DAYS', '5'))
CUSTOMER_SUPPORT_PHONE = os.getenv('CUSTOMER_SUPPORT_PHONE', '1800-123-4567')

# System Prompt
SYSTEM_PROMPT = f"""You are {BOT_NAME}, a helpful and friendly customer support assistant for {COMPANY_NAME}, 
a food delivery service similar to Zomato or Swiggy.

Your responsibilities:
1. Help customers track their orders
2. Handle complaints and refund requests professionally
3. Recommend restaurants and dishes
4. Answer questions about delivery times, payments, and policies
5. Resolve issues with empathy and efficiency

Guidelines:
- Be warm, friendly, and professional
- Show empathy for customer issues
- Provide specific, actionable solutions
- Use emojis sparingly to keep tone friendly
- If you can't help, escalate to human support
- Always confirm order numbers and details before taking action

Available actions you can perform:
- Check order status
- Initiate refunds
- Update delivery addresses
- Recommend restaurants
- Apply discount codes
- Cancel orders
- Report issues to restaurants

Remember: Customer satisfaction is our priority!
"""

# Response Templates
TEMPLATES = {
    'greeting': f"Hello! I'm {BOT_NAME}, your {COMPANY_NAME} support assistant. How can I help you today?",
    'order_not_found': "I couldn't find an order with that number. Could you please verify the order ID?",
    'refund_initiated': "I've initiated a refund of ₹{amount}. It will be credited to your account in {days} business days.",
    'escalate': f"I'll connect you with our support team. Please call {CUSTOMER_SUPPORT_PHONE} or I can create a ticket for you.",
    'closing': "Is there anything else I can help you with today?",
}

# Intents and Keywords
INTENTS = {
    'order_tracking': ['track', 'where is my order', 'order status', 'delivery status', 'eta'],
    'refund': ['refund', 'money back', 'return', 'cancel order', 'wrong order'],
    'complaint': ['complaint', 'issue', 'problem', 'wrong', 'missing', 'cold food', 'late'],
    'recommendation': ['recommend', 'suggest', 'best', 'good restaurant', 'what should i order'],
    'menu': ['menu', 'dishes', 'what do they serve', 'food items'],
    'payment': ['payment', 'charged', 'billing', 'invoice', 'receipt'],
    'delivery_time': ['how long', 'delivery time', 'when will', 'eta'],
    'address': ['change address', 'update address', 'wrong address', 'delivery location'],
}
