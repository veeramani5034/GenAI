"""
Streamlit Web Interface for Food Delivery Chatbot
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from chatbot import FoodDeliveryChatbot
import config

# Page configuration
st.set_page_config(
    page_title=f"{config.BOT_NAME} - Customer Support",
    page_icon="🍕",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        align-items: flex-end;
    }
    .bot-message {
        background-color: #f5f5f5;
        align-items: flex-start;
    }
    .message-content {
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = FoodDeliveryChatbot()
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title(f"🍕 {config.COMPANY_NAME}")
    st.subheader("Customer Support")
    
    st.markdown("---")
    
    st.markdown("### Quick Actions")
    if st.button("🔄 New Conversation"):
        st.session_state.chatbot.reset_conversation()
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### Sample Queries")
    st.markdown("""
    - Track my order #12345
    - I want a refund for order #12346
    - Recommend a good pizza place
    - What's the status of my delivery?
    - Change my delivery address
    """)
    
    st.markdown("---")
    
    st.markdown("### Contact Support")
    st.info(f"📞 {config.CUSTOMER_SUPPORT_PHONE}")
    
    st.markdown("---")
    
    st.markdown("### About")
    st.caption(f"""
    {config.BOT_NAME} is an AI-powered customer support assistant 
    designed to help you with orders, refunds, and recommendations.
    """)

# Main chat interface
st.title(f"💬 {config.BOT_NAME}")
st.caption(f"Your {config.COMPANY_NAME} Support Assistant")

# Display chat messages
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.info(config.TEMPLATES['greeting'])
    
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-content">
                    <strong>You:</strong><br>{content}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-content">
                    <strong>{config.BOT_NAME}:</strong><br>{content}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get bot response
    with st.spinner(f"{config.BOT_NAME} is typing..."):
        try:
            response = st.session_state.chatbot.chat(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_message = f"I'm sorry, I encountered an error. Please try again or contact support at {config.CUSTOMER_SUPPORT_PHONE}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.error(f"Error: {str(e)}")
    
    # Rerun to update chat display
    st.rerun()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Response Time", "< 2 sec")

with col2:
    st.metric("Satisfaction", "4.8/5.0")

with col3:
    st.metric("Issues Resolved", "95%")
