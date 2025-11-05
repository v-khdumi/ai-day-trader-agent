# Quick Start Guide - AI Day Trader Agent GUI

## 🚀 Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Create a `.env` file in the project root:
```env
TWELVE_DATA_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### 3. Launch the GUI
**Easiest method:**
```bash
python launch_gui.py
```

**Alternative methods:**
```bash
# Linux/Mac
./start_gui.sh

# Windows
start_gui.bat

# Direct streamlit command
streamlit run gui_app.py
```

---

## 📱 First Time Setup

When you first open the GUI:

1. **Go to Portfolio Management** → Portfolio Settings
2. **Click "Create New Portfolio"**
3. Enter a name (e.g., "My Portfolio") and trading capital
4. Start adding holdings or analyzing stocks!

---

## 🎯 Common Tasks

### Analyze a Stock
1. Go to **🔍 Stock Analysis**
2. Enter ticker symbol (e.g., AAPL)
3. Click **Analyze**
4. Review recommendation and click **Execute** if desired

### View Portfolio Performance
1. Go to **📊 Dashboard**
2. See total value, holdings, and performance
3. View charts for allocation and P&L

### Add Holdings
1. Go to **💼 Portfolio Management** → Add/Edit Holdings
2. Enter symbol, quantity, and average cost
3. Click **Save Holding**

### Review Trade History
1. Go to **📈 Trade History**
2. Select time period
3. View trades and analytics

---

## ⚡ Keyboard Shortcuts

- `R` - Refresh page
- `Ctrl/Cmd + K` - Open command palette
- `Ctrl/Cmd + Q` - Stop server

---

## ❓ Troubleshooting

**GUI won't start?**
- Make sure Streamlit is installed: `pip install streamlit`
- Check port 8501 is available
- Try a different port in `.streamlit/config.toml`

**Can't analyze stocks?**
- Verify API keys in `.env` file
- Check Settings page for key status
- Ensure internet connection is active

**Portfolio not showing?**
- Create a portfolio in Portfolio Management
- Select it from the sidebar dropdown

**Trade execution fails?**
- Ensure portfolio has sufficient cash
- Verify stock symbol is correct
- Check API rate limits

---

## 📞 Need Help?

- Check `GUI_GUIDE.md` for detailed documentation
- Review `README.md` for setup instructions
- See `API_DOCUMENTATION.md` for technical details

---

## 💡 Pro Tips

✅ Use the **Dashboard** to get a quick overview before trading
✅ Always check **confidence levels** before executing trades
✅ Review **all strategy signals** not just the primary one
✅ Set up **multiple portfolios** for different strategies
✅ Regularly check **Trade History** to track performance
✅ Back up your database using CLI commands
✅ Monitor **API key status** in Settings

---

**Happy Trading! 📈🤖**
