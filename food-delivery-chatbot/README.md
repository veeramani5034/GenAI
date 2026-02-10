# Food Delivery Customer Support Chatbot

AI-powered customer support chatbot for food delivery services (like Zomato/Swiggy) using OpenAI GPT and LangChain.

## Features

- 🤖 Natural language understanding
- 📦 Order tracking and status
- 🍕 Menu queries and recommendations
- 💰 Refund and complaint handling
- 🚚 Delivery time estimates
- 📍 Address management
- 💳 Payment issues
- ⭐ Restaurant recommendations

## Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API Key

### Installation

```bash
# 1. Navigate to project
cd food-delivery-chatbot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env and add your OpenAI API key

# 5. Run the chatbot
python chatbot.py
```

## Usage

### Command Line Interface

```bash
python chatbot.py
```

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

Access at: http://localhost:8501

## Example Conversations

**Order Tracking:**
```
User: Where is my order #12345?
Bot: Let me check that for you... Your order #12345 is currently being prepared 
     at the restaurant. Estimated delivery time is 25 minutes.
```

**Refund Request:**
```
User: I want a refund for my last order
Bot: I'm sorry to hear that. Can you tell me what went wrong with your order?
User: The food was cold
Bot: I understand. I've initiated a refund of ₹450 to your original payment method.
     It will reflect in 3-5 business days.
```

**Restaurant Recommendation:**
```
User: Suggest a good pizza place
Bot: Based on your location and preferences, I recommend:
     1. Pizza Paradise - 4.5★ (30 min delivery)
     2. Italiano Express - 4.3★ (25 min delivery)
```

## Project Structure

```
food-delivery-chatbot/
├── chatbot.py              # Main chatbot logic
├── app.py                  # Streamlit web interface
├── config.py               # Configuration
├── data/
│   ├── orders.json         # Sample order data
│   ├── restaurants.json    # Restaurant database
│   └── menu.json          # Menu items
├── utils/
│   ├── order_manager.py    # Order operations
│   ├── restaurant_db.py    # Restaurant queries
│   └── conversation.py     # Conversation handling
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Customization

Edit `config.py` to customize:
- Bot personality
- Response templates
- Business rules
- Supported features

## Deployment

### Local
```bash
python chatbot.py
```

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy

### Docker
```bash
docker build -t food-chatbot .
docker run -p 8501:8501 food-chatbot
```

## License

MIT License
