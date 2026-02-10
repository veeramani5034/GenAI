"""
Food Delivery Customer Support Chatbot
Main chatbot logic using OpenAI and LangChain
"""

import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Add utils to path
sys.path.append(os.path.dirname(__file__))

from utils.order_manager import OrderManager
from utils.restaurant_db import RestaurantDB
import config

load_dotenv()


class FoodDeliveryChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=config.MODEL,
            temperature=config.TEMPERATURE,
            openai_api_key=config.OPENAI_API_KEY
        )
        self.order_manager = OrderManager()
        self.restaurant_db = RestaurantDB()
        self.conversation_history = []
        
        # Initialize with system prompt
        self.conversation_history.append(
            SystemMessage(content=config.SYSTEM_PROMPT)
        )
    
    def extract_order_id(self, text):
        """Extract order ID from user message"""
        import re
        # Look for patterns like #12345, 12345, order 12345
        patterns = [
            r'#(\d+)',
            r'order\s+(\d+)',
            r'\b(\d{5})\b'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def handle_order_tracking(self, user_message):
        """Handle order tracking queries"""
        order_id = self.extract_order_id(user_message)
        
        if not order_id:
            return "Could you please provide your order number? It's a 5-digit number like #12345."
        
        order_status = self.order_manager.get_order_status(order_id)
        
        if not order_status:
            return config.TEMPLATES['order_not_found']
        
        response = f"""
📦 **Order #{order_status['order_id']}**

Restaurant: {order_status['restaurant']}
Items: {', '.join(order_status['items'])}
Total: ₹{order_status['total']}

Status: {order_status['status_message']}
Estimated Delivery: {order_status['estimated_delivery']}
Delivery Address: {order_status['delivery_address']}
"""
        return response
    
    def handle_refund_request(self, user_message, order_id=None):
        """Handle refund requests"""
        if not order_id:
            order_id = self.extract_order_id(user_message)
        
        if not order_id:
            return "I'd be happy to help with a refund. Could you please provide your order number?"
        
        order = self.order_manager.get_order(order_id)
        if not order:
            return config.TEMPLATES['order_not_found']
        
        # Extract reason from message
        reason = "Customer requested refund"
        
        refund_info = self.order_manager.initiate_refund(order_id, reason)
        
        if refund_info:
            return config.TEMPLATES['refund_initiated'].format(
                amount=refund_info['amount'],
                days=config.REFUND_PROCESSING_DAYS
            ) + f"\n\nReference ID: {refund_info['order_id']}-REF"
        
        return "I'm sorry, I couldn't process the refund. Let me connect you with our support team."
    
    def handle_restaurant_recommendation(self, user_message):
        """Handle restaurant recommendations"""
        # Simple keyword extraction
        preferences = {}
        
        cuisines = ['pizza', 'biryani', 'burger', 'chinese', 'south indian', 'sushi', 'mexican', 'healthy']
        for cuisine in cuisines:
            if cuisine in user_message.lower():
                preferences['cuisine'] = cuisine
                break
        
        restaurants = self.restaurant_db.recommend_restaurants(preferences)
        
        if not restaurants:
            restaurants = self.restaurant_db.get_top_rated(3)
        
        response = "Here are some great options for you:\n\n"
        for i, restaurant in enumerate(restaurants, 1):
            response += f"{i}. {self.restaurant_db.format_restaurant_info(restaurant)}\n"
        
        return response
    
    def detect_intent(self, user_message):
        """Detect user intent from message"""
        message_lower = user_message.lower()
        
        for intent, keywords in config.INTENTS.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return 'general'
    
    def get_context_info(self, intent, user_message):
        """Get relevant context information based on intent"""
        context = ""
        
        if intent == 'order_tracking':
            order_id = self.extract_order_id(user_message)
            if order_id:
                order_status = self.order_manager.get_order_status(order_id)
                if order_status:
                    context = f"\n\nOrder Information:\n{order_status}"
        
        elif intent == 'recommendation':
            top_restaurants = self.restaurant_db.get_top_rated(5)
            context = f"\n\nTop Restaurants:\n{top_restaurants}"
        
        return context
    
    def chat(self, user_message):
        """Main chat method"""
        # Detect intent
        intent = self.detect_intent(user_message)
        
        # Handle specific intents with direct actions
        if intent == 'order_tracking':
            order_id = self.extract_order_id(user_message)
            if order_id:
                return self.handle_order_tracking(user_message)
        
        elif intent == 'refund':
            order_id = self.extract_order_id(user_message)
            if order_id:
                return self.handle_refund_request(user_message, order_id)
        
        elif intent == 'recommendation':
            return self.handle_restaurant_recommendation(user_message)
        
        # For other intents, use LLM with context
        context_info = self.get_context_info(intent, user_message)
        
        # Add user message to history
        enhanced_message = user_message
        if context_info:
            enhanced_message += context_info
        
        self.conversation_history.append(HumanMessage(content=enhanced_message))
        
        # Get response from LLM
        response = self.llm.invoke(self.conversation_history)
        
        # Add AI response to history
        self.conversation_history.append(AIMessage(content=response.content))
        
        return response.content
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = [
            SystemMessage(content=config.SYSTEM_PROMPT)
        ]


def main():
    """Command-line interface for the chatbot"""
    print("=" * 60)
    print(f"  {config.BOT_NAME} - {config.COMPANY_NAME} Customer Support")
    print("=" * 60)
    print(f"\n{config.TEMPLATES['greeting']}\n")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    chatbot = FoodDeliveryChatbot()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n{config.BOT_NAME}: Thank you for contacting {config.COMPANY_NAME}! Have a great day! 👋\n")
                break
            
            if user_input.lower() == 'reset':
                chatbot.reset_conversation()
                print(f"\n{config.BOT_NAME}: Conversation reset. How can I help you?\n")
                continue
            
            response = chatbot.chat(user_input)
            print(f"\n{config.BOT_NAME}: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{config.BOT_NAME}: Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"\n{config.BOT_NAME}: I'm sorry, I encountered an error. Please try again or contact support at {config.CUSTOMER_SUPPORT_PHONE}\n")
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
