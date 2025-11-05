# GUI User Guide

## AI Day Trader Agent - Graphical User Interface

This guide explains how to use the web-based graphical user interface for the AI Day Trader Agent.

---

## Quick Start

### Starting the GUI

**Option 1: Using startup scripts**

Linux/Mac:
```bash
./start_gui.sh
```

Windows:
```cmd
start_gui.bat
```

**Option 2: Manual start**
```bash
streamlit run gui_app.py
```

The GUI will automatically open in your default browser at `http://localhost:8501`

---

## GUI Features

### 📊 Dashboard

The main dashboard provides a comprehensive overview of your portfolio:

- **Portfolio Metrics**
  - Total portfolio value
  - Cash available for trading
  - Holdings value
  - Win rate and performance metrics

- **Holdings Overview**
  - Current positions with real-time data
  - Unrealized profit/loss per position
  - Visual distribution charts

- **Performance Analytics**
  - Total return tracking
  - Realized and unrealized P&L
  - Trade statistics

### 🔍 Stock Analysis

Analyze any stock symbol with AI-powered recommendations:

1. **Enter Stock Symbol**: Type the ticker symbol (e.g., AAPL, MSFT, TSLA)
2. **Click Analyze**: Get comprehensive analysis including:
   - Buy/Sell/Hold recommendation
   - Confidence level
   - Recommended quantity
   - Technical indicators (RSI, MACD, SMA, EMA)
   - Sentiment analysis
   - Dividend capture opportunities
   - Risk management (stop-loss, take-profit)

3. **Execute Trades**: One-click trade execution directly from the analysis page

### 💼 Portfolio Management

Manage your portfolios and holdings:

#### Overview Tab
- View complete portfolio details
- See all current holdings with performance metrics
- Remove holdings with a single click

#### Add/Edit Holdings Tab
- Add new holdings to your portfolio
- Update existing positions
- Set average cost basis for accurate P&L tracking

#### Portfolio Settings Tab
- Create new portfolios
- Update trading capital
- Configure portfolio parameters

### 📈 Trade History

Review your trading activity:

- **Filterable History**: View trades by time period (7, 30, 90, 180, 365 days)
- **Trade Statistics**: See buy/sell distribution and total volume
- **Visual Analytics**:
  - Trade distribution pie charts
  - Strategy performance charts
- **Detailed Trade Log**: Complete transaction details with timestamps

### ⚙️ Settings

Monitor system configuration:

- **API Key Status**: Check which API keys are configured
- **Trading Parameters**: View default capital and position sizing rules
- **Application Info**: Version and feature information

---

## Tips for Best Results

### Portfolio Setup
1. Start by creating a portfolio in **Portfolio Management > Portfolio Settings**
2. Add your current holdings with accurate cost basis
3. Use the dashboard to monitor performance

### Stock Analysis
1. Always check multiple indicators before making decisions
2. Pay attention to confidence levels
3. Review risk management parameters (stop-loss, take-profit)
4. Consider all strategy signals (Technical, Sentiment, Dividend)

### Trade Execution
1. Review the analysis carefully before executing
2. Trades are recorded in your portfolio automatically
3. Check trade history to track performance

### Data Management
1. The GUI uses the same database as the CLI
2. Changes made in the GUI are immediately reflected in CLI
3. Back up your portfolio data regularly using CLI commands

---

## Troubleshooting

### GUI Won't Start
- Ensure Streamlit is installed: `pip install streamlit plotly`
- Check that port 8501 is not in use
- Verify your Python environment is activated

### Missing API Keys
- Create a `.env` file in the project root
- Add all required API keys (see README.md)
- Restart the GUI after adding keys

### Data Not Showing
- Ensure you've created a portfolio
- Check that API keys are configured correctly
- Verify internet connection for real-time data

### Analysis Errors
- Verify the stock symbol is correct
- Check API rate limits in Settings
- Ensure all required API keys are configured

---

## Navigation Tips

- **Sidebar**: Use the sidebar to switch between pages and select portfolios
- **Page Tabs**: Some pages have tabs for different features
- **Expandable Sections**: Click to expand/collapse detailed information
- **Refresh**: The page auto-updates after actions, or use the Streamlit refresh button

---

## Security Notes

⚠️ **Important Security Guidelines:**

1. **Never share your `.env` file** - it contains sensitive API keys
2. **Run locally** - the GUI is designed for local use only
3. **Secure your database** - contains your portfolio and trade data
4. **API keys** - visible status but values are masked in the GUI

---

## Integration with Other Interfaces

The GUI works seamlessly with other interfaces:

- **CLI**: Use `python run.py` for command-line operations
- **API Server**: Run `python api_server.py` for REST API access
- **Discord Bot**: Use `python core/discord_bot.py` for Discord integration

All interfaces share the same database, so your data is consistent across platforms.

---

## Advanced Features

### Real-Time Updates
- Portfolio values update when you refresh or perform actions
- Trade history updates automatically after execution

### Multi-Portfolio Support
- Create multiple portfolios for different strategies
- Switch between portfolios using the sidebar selector
- Each portfolio maintains independent holdings and capital

### Interactive Charts
- Hover over charts for detailed information
- Charts are interactive and responsive
- Visual analytics help identify trends

---

## Support

For issues or questions:
1. Check the main README.md for setup instructions
2. Review the API_DOCUMENTATION.md for API details
3. Check the CHANGELOG.md for version updates
4. Report issues on the GitHub repository

---

**Enjoy trading with AI-powered insights!** 📈🤖
