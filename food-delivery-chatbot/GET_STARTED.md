# Get Started in 5 Minutes! 🚀

Quick guide to get your food delivery chatbot running.

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] OpenAI API key (get from https://platform.openai.com/api-keys)
- [ ] 5 minutes of your time!

## Super Quick Start

```bash
# 1. Navigate to project
cd food-delivery-chatbot

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 4. Install packages
pip install -r requirements.txt

# 5. Setup environment
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# 6. Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# 7. Run quick start check
python quick_start.py

# 8. Launch web interface
streamlit run app.py
```

That's it! Your chatbot is now running at http://localhost:8501

## Test It Out

Try these sample queries:

1. **Order Tracking:**
   ```
   Where is my order #12345?
   ```

2. **Refund Request:**
   ```
   I want a refund for order #12346
   ```

3. **Restaurant Recommendation:**
   ```
   Suggest a good pizza place
   ```

4. **General Query:**
   ```
   What's your refund policy?
   ```

## Sample Order IDs

Use these for testing:
- `12345` - Pizza order (preparing)
- `12346` - Biryani order (out for delivery)
- `12347` - Burger order (delivered)
- `12348` - Dosa order (preparing)
- `12349` - Chinese order (confirmed)

## Two Ways to Run

### 1. Web Interface (Recommended) 🌐

```bash
streamlit run app.py
```

- Beautiful UI
- Easy to use
- Mobile responsive
- Best for demos

### 2. Command Line 💻

```bash
python chatbot.py
```

- Terminal-based
- Quick testing
- Developer-friendly
- Lightweight

## Common Issues & Quick Fixes

### Issue: "No module named 'openai'"

**Fix:**
```bash
pip install -r requirements.txt
```

### Issue: "OpenAI API key not found"

**Fix:**
1. Make sure `.env` file exists
2. Add your API key: `OPENAI_API_KEY=sk-...`
3. No spaces around the `=`

### Issue: "Port 8501 already in use"

**Fix:**
```bash
streamlit run app.py --server.port 8502
```

## What's Included

```
food-delivery-chatbot/
├── 📱 app.py                  # Web interface
├── 🤖 chatbot.py              # Core chatbot
├── ⚙️ config.py               # Settings
├── 📊 data/
│   ├── orders.json           # Sample orders
│   └── restaurants.json      # Restaurant data
└── 🛠️ utils/
    ├── order_manager.py      # Order operations
    └── restaurant_db.py      # Restaurant queries
```

## Next Steps

1. ✅ **Test all features** - Try different queries
2. 🎨 **Customize** - Edit config.py for your brand
3. 📝 **Add data** - Update restaurants.json with your data
4. 🚀 **Deploy** - Push to Streamlit Cloud
5. 📈 **Extend** - Add more features!

## Need Help?

- 📖 **Detailed Setup:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🎯 **Features:** See [FEATURES.md](FEATURES.md)
- 📚 **Full Docs:** See [README.md](README.md)

## Quick Customization

### Change Bot Name

Edit `.env`:
```
BOT_NAME=MyBot
COMPANY_NAME=MyCompany
```

### Add Restaurant

Edit `data/restaurants.json`:
```json
{
  "id": 9,
  "name": "New Restaurant",
  "cuisine": ["Italian"],
  "rating": 4.5,
  "delivery_time": "30 min",
  "popular_dishes": ["Pasta", "Pizza"]
}
```

### Modify Personality

Edit `config.py` → `SYSTEM_PROMPT`

## Deploy to Cloud

### Streamlit Cloud (Free!)

1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Add OpenAI key in secrets
5. Deploy!

## Success Checklist

After setup, you should be able to:

- [ ] Open web interface at http://localhost:8501
- [ ] Track order #12345
- [ ] Get restaurant recommendations
- [ ] Request refunds
- [ ] Chat naturally with the bot

## That's It! 🎉

You now have a working AI customer support chatbot!

**Questions?** Check the other documentation files or open an issue.

**Happy Chatting!** 🤖💬
