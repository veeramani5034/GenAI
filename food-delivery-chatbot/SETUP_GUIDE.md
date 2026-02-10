# Setup Guide - Food Delivery Chatbot

Complete step-by-step guide to set up and run the chatbot.

## Prerequisites

- Python 3.9 or higher
- OpenAI API Key (get from https://platform.openai.com/api-keys)
- pip (Python package manager)

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd food-delivery-chatbot
```

### 2. Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- openai
- langchain
- streamlit
- python-dotenv
- pandas

### 4. Configure Environment

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env file and add your OpenAI API key
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
BOT_NAME=FoodBot
COMPANY_NAME=QuickBite
MODEL=gpt-4
TEMPERATURE=0.7
```

### 5. Verify Installation

```bash
python -c "import openai; import langchain; import streamlit; print('All packages installed!')"
```

## Running the Chatbot

### Option 1: Command Line Interface

```bash
python chatbot.py
```

This opens an interactive chat in your terminal.

**Example conversation:**
```
You: Track my order #12345
FoodBot: Your order #12345 is being prepared...

You: Recommend a pizza place
FoodBot: Here are some great options...
```

### Option 2: Web Interface (Recommended)

```bash
streamlit run app.py
```

This opens a web browser at http://localhost:8501 with a beautiful chat interface.

## Testing the Chatbot

### Test Order Tracking

```
User: Where is my order #12345?
```

Expected: Bot shows order status, items, delivery time

### Test Refund Request

```
User: I want a refund for order #12346
```

Expected: Bot initiates refund and provides reference number

### Test Restaurant Recommendation

```
User: Suggest a good biryani place
```

Expected: Bot recommends restaurants with biryani

### Test General Query

```
User: What's your refund policy?
```

Expected: Bot explains refund policy

## Sample Order IDs for Testing

- `12345` - Pizza order (preparing)
- `12346` - Biryani order (out for delivery)
- `12347` - Burger order (delivered)
- `12348` - Dosa order (preparing)
- `12349` - Chinese order (confirmed)

## Customization

### Change Bot Name

Edit `.env`:
```
BOT_NAME=YourBotName
COMPANY_NAME=YourCompany
```

### Add More Restaurants

Edit `data/restaurants.json` and add new entries:
```json
{
  "id": 9,
  "name": "Your Restaurant",
  "cuisine": ["Italian"],
  "rating": 4.5,
  "delivery_time": "30 min",
  "min_order": 200,
  "popular_dishes": ["Pasta", "Pizza"],
  "location": "Downtown",
  "price_range": "₹₹"
}
```

### Add More Orders

Edit `data/orders.json` and add new test orders.

### Modify Bot Personality

Edit `config.py` and update `SYSTEM_PROMPT`:
```python
SYSTEM_PROMPT = """You are a friendly chatbot..."""
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall packages
pip install -r requirements.txt
```

### Issue: OpenAI API Error

**Solution:**
- Check your API key in `.env`
- Verify you have credits: https://platform.openai.com/usage
- Ensure no extra spaces in the API key

### Issue: Streamlit won't start

**Solution:**
```bash
# Check if port 8501 is available
# Try a different port
streamlit run app.py --server.port 8502
```

### Issue: Can't find data files

**Solution:**
Make sure you're running from the `food-delivery-chatbot` directory:
```bash
cd food-delivery-chatbot
python chatbot.py
```

## Project Structure

```
food-delivery-chatbot/
├── chatbot.py              # Main chatbot logic
├── app.py                  # Streamlit web interface
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── .env                   # Your config (create this)
├── data/
│   ├── orders.json        # Sample orders
│   └── restaurants.json   # Restaurant database
└── utils/
    ├── order_manager.py   # Order operations
    └── restaurant_db.py   # Restaurant queries
```

## Next Steps

1. **Test all features** - Try different queries
2. **Customize data** - Add your own restaurants and orders
3. **Modify personality** - Adjust the bot's tone in config.py
4. **Deploy** - Deploy to Streamlit Cloud or your server
5. **Extend** - Add more features like payment integration

## Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Add your OpenAI API key in secrets
5. Deploy!

### Run on Server

```bash
# Install screen or tmux
screen -S chatbot

# Run streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# Detach: Ctrl+A, D
```

## Support

If you encounter issues:
1. Check this guide
2. Verify all prerequisites are installed
3. Ensure `.env` is configured correctly
4. Check that data files exist

## License

MIT License - Feel free to modify and use!
