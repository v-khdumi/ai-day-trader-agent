#!/usr/bin/env python3
"""
Streamlit-based Graphical User Interface for AI Day Trader Agent.
Provides an intuitive web-based interface for portfolio management and trading analysis.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.env_loader import load_env_variables
from core.pipeline import EnhancedTradingPipeline
from core.portfolio_manager import PortfolioManager
from utils.logger import get_logger

# Page configuration
st.set_page_config(
    page_title="AI Day Trader Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize logger
logger = get_logger('gui_app')

# Session state initialization
if 'portfolio_manager' not in st.session_state:
    st.session_state.portfolio_manager = PortfolioManager()
if 'selected_portfolio' not in st.session_state:
    st.session_state.selected_portfolio = "default"
if 'api_keys' not in st.session_state:
    try:
        st.session_state.api_keys = load_env_variables()
    except Exception as e:
        logger.warning(f"Could not load all API keys: {e}")
        # Initialize with empty dict to allow GUI to start
        st.session_state.api_keys = {}
        st.session_state.api_keys_error = str(e)


def show_sidebar():
    """Display the sidebar navigation."""
    with st.sidebar:
        st.title("🤖 AI Day Trader")
        st.markdown("---")
        
        # Portfolio selector
        portfolios = st.session_state.portfolio_manager.list_portfolios()
        portfolio_names = [p['name'] for p in portfolios] if portfolios else ["default"]
        
        if "default" not in portfolio_names:
            portfolio_names.insert(0, "default")
        
        st.session_state.selected_portfolio = st.selectbox(
            "Select Portfolio",
            portfolio_names,
            index=portfolio_names.index(st.session_state.selected_portfolio) 
                  if st.session_state.selected_portfolio in portfolio_names else 0
        )
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "🔍 Stock Analysis", "💼 Portfolio Management", 
             "📈 Trade History", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.caption("AI-powered trading recommendations")
        
        return page


def format_currency(value: float) -> str:
    """Format number as currency."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Format number as percentage."""
    return f"{value:+.2f}%"


def show_dashboard():
    """Display the main dashboard."""
    st.title("📊 Portfolio Dashboard")
    
    pm = st.session_state.portfolio_manager
    portfolio_name = st.session_state.selected_portfolio
    
    # Get portfolio data
    portfolio = pm.get_portfolio(portfolio_name)
    
    if not portfolio:
        st.warning(f"Portfolio '{portfolio_name}' not found. Create one in Portfolio Management.")
        return
    
    value_info = pm.get_portfolio_value(portfolio_name)
    metrics = pm.get_performance_metrics(portfolio_name)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Value",
            format_currency(value_info['total_value']),
            delta=format_currency(metrics['total_return']) if metrics else None
        )
    
    with col2:
        st.metric(
            "Cash Available",
            format_currency(value_info['cash_available'])
        )
    
    with col3:
        st.metric(
            "Holdings Value",
            format_currency(value_info['holdings_value'])
        )
    
    with col4:
        if metrics and metrics['total_trades'] > 0:
            st.metric(
                "Win Rate",
                f"{metrics['win_rate']:.1f}%",
                delta=f"{metrics['total_trades']} trades"
            )
        else:
            st.metric("Win Rate", "N/A", delta="No trades yet")
    
    st.markdown("---")
    
    # Holdings overview
    if value_info['holdings_details']:
        st.subheader("📈 Current Holdings")
        
        # Create DataFrame for holdings
        holdings_data = []
        for holding in value_info['holdings_details']:
            holdings_data.append({
                'Symbol': holding['symbol'],
                'Quantity': holding['quantity'],
                'Avg Cost': format_currency(holding['avg_cost']),
                'Current Price': format_currency(holding['current_price']),
                'Market Value': format_currency(holding['market_value']),
                'Unrealized P&L': format_currency(holding['unrealized_pnl']),
                'P&L %': format_percentage(holding['unrealized_pnl_pct'])
            })
        
        df = pd.DataFrame(holdings_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Holdings distribution pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Holdings Distribution")
            fig = px.pie(
                values=[h['market_value'] for h in value_info['holdings_details']],
                names=[h['symbol'] for h in value_info['holdings_details']],
                title="Portfolio Allocation"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Performance by Position")
            symbols = [h['symbol'] for h in value_info['holdings_details']]
            pnl_pcts = [h['unrealized_pnl_pct'] for h in value_info['holdings_details']]
            
            fig = go.Figure(data=[
                go.Bar(
                    x=symbols,
                    y=pnl_pcts,
                    marker_color=['green' if p >= 0 else 'red' for p in pnl_pcts]
                )
            ])
            fig.update_layout(
                title="Unrealized P&L by Position (%)",
                xaxis_title="Symbol",
                yaxis_title="P&L %",
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No holdings in portfolio. Use Stock Analysis to get trading recommendations.")
    
    # Performance metrics
    if metrics:
        st.markdown("---")
        st.subheader("📊 Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Return", format_currency(metrics['total_return']))
        
        with col2:
            st.metric("Realized P&L", format_currency(metrics['realized_pnl']))
        
        with col3:
            st.metric("Unrealized P&L", format_currency(metrics['unrealized_pnl']))
        
        with col4:
            st.metric("Total Trades", metrics['total_trades'])


def show_stock_analysis():
    """Display stock analysis interface."""
    st.title("🔍 Stock Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ticker = st.text_input(
            "Enter Stock Symbol",
            placeholder="e.g., AAPL, MSFT, TSLA",
            help="Enter a stock ticker symbol to analyze"
        ).upper()
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        analyze_button = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
    if analyze_button and ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                # Initialize pipeline
                pipeline = EnhancedTradingPipeline(
                    ticker,
                    st.session_state.selected_portfolio
                )
                
                # Run analysis
                result = pipeline.run_analysis(st.session_state.api_keys)
                
                # Check for errors
                if result.get('error'):
                    st.error(f"Analysis failed: {result.get('message', 'Unknown error')}")
                    return
                
                # Display results
                st.success("✅ Analysis Complete!")
                
                # Key recommendation
                col1, col2, col3 = st.columns(3)
                
                signal = result.get('signal', 'HOLD')
                signal_color = {
                    'BUY': '🟢',
                    'SELL': '🔴',
                    'HOLD': '🟡'
                }.get(signal, '⚪')
                
                with col1:
                    st.metric("Recommendation", f"{signal_color} {signal}")
                
                with col2:
                    confidence = result.get('confidence', '0%')
                    try:
                        if isinstance(confidence, str):
                            conf_display = confidence
                        elif isinstance(confidence, (int, float)):
                            conf_display = f"{confidence:.1%}"
                        else:
                            conf_display = "N/A"
                    except (ValueError, TypeError):
                        conf_display = "N/A"
                    st.metric("Confidence", conf_display)
                
                with col3:
                    quantity = result.get('quantity', 0)
                    st.metric("Quantity", f"{quantity} shares")
                
                st.markdown("---")
                
                # Detailed analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Analysis Details")
                    st.write(f"**Primary Strategy:** {result.get('primary_strategy', 'N/A')}")
                    st.write(f"**Reason:** {result.get('primary_reason', 'N/A')}")
                    
                    # Technical indicators
                    technical = result.get('all_signals', {}).get('technical', {})
                    if technical:
                        st.subheader("📊 Technical Indicators")
                        
                        price = technical.get('current_price', 0)
                        st.write(f"**Current Price:** ${price:.2f}")
                        
                        rsi = technical.get('rsi', 0)
                        rsi_label = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
                        st.write(f"**RSI:** {rsi:.2f} ({rsi_label})")
                        
                        macd = technical.get('macd', 0)
                        macd_signal = technical.get('macd_signal', 0)
                        macd_trend = "Bullish" if macd > macd_signal else "Bearish"
                        st.write(f"**MACD:** {macd:.4f} / Signal: {macd_signal:.4f} ({macd_trend})")
                        
                        sma = technical.get('sma_20', 0)
                        sma_pos = "Above" if price > sma else "Below"
                        st.write(f"**SMA(20):** ${sma:.2f} ({sma_pos})")
                        
                        ema = technical.get('ema_20', 0)
                        ema_pos = "Above" if price > ema else "Below"
                        st.write(f"**EMA(20):** ${ema:.2f} ({ema_pos})")
                
                with col2:
                    st.subheader("📈 All Strategy Signals")
                    
                    all_signals = result.get('all_signals', {})
                    
                    # Technical signal
                    tech_signal = all_signals.get('technical', {})
                    if tech_signal:
                        tech_rec = tech_signal.get('recommendation', 'HOLD')
                        tech_strength = tech_signal.get('signal_strength', 0)
                        st.write(f"**Technical:** {tech_rec} (strength: {tech_strength:.2f})")
                    
                    # Sentiment signal
                    sent_signal = all_signals.get('sentiment', {})
                    if sent_signal:
                        sent_rec = sent_signal.get('recommendation', 'HOLD')
                        sent_score = sent_signal.get('score', 0)
                        st.write(f"**Sentiment:** {sent_rec} (score: {sent_score:.2f})")
                    
                    # Dividend signal
                    div_signal = all_signals.get('dividend', {})
                    if div_signal:
                        div_rec = div_signal.get('recommendation', 'HOLD')
                        div_reason = div_signal.get('reason', 'N/A')
                        st.write(f"**Dividend:** {div_rec}")
                        st.caption(div_reason)
                    
                    # Risk management
                    st.subheader("⚠️ Risk Management")
                    stop_loss = result.get('stop_loss')
                    take_profit = result.get('take_profit')
                    
                    if stop_loss:
                        st.write(f"**Stop Loss:** ${stop_loss:.2f}")
                    if take_profit:
                        st.write(f"**Take Profit:** ${take_profit:.2f}")
                
                # Action button
                if signal in ['BUY', 'SELL'] and quantity > 0:
                    st.markdown("---")
                    st.subheader("💼 Execute Trade")
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.info(f"Recommendation: {signal} {quantity} shares of {ticker}")
                    
                    with col2:
                        if st.button("✅ Execute Trade", type="primary", use_container_width=True):
                            try:
                                pm = st.session_state.portfolio_manager
                                current_price = technical.get('current_price', 0)
                                
                                if current_price > 0:
                                    # Parse confidence value safely
                                    confidence_value = result.get('confidence', 0)
                                    try:
                                        if isinstance(confidence_value, str):
                                            # Remove % and convert to float
                                            confidence_float = float(confidence_value.rstrip('%')) / 100
                                        elif isinstance(confidence_value, (int, float)):
                                            confidence_float = float(confidence_value)
                                        else:
                                            confidence_float = 0.0
                                    except (ValueError, AttributeError):
                                        confidence_float = 0.0
                                    
                                    trade_id = pm.record_trade(
                                        name=st.session_state.selected_portfolio,
                                        symbol=ticker,
                                        action=signal,
                                        quantity=quantity,
                                        price=current_price,
                                        strategy=result.get('primary_strategy', 'multi'),
                                        confidence=confidence_float,
                                        notes=f"GUI execution: {result.get('primary_reason', '')}"
                                    )
                                    st.success(f"✅ Trade executed! Trade ID: {trade_id}")
                                    st.rerun()
                                else:
                                    st.error("Cannot execute: price unavailable")
                            except Exception as e:
                                st.error(f"Trade execution failed: {e}")
                    
                    with col3:
                        if st.button("❌ Cancel"):
                            st.info("Trade cancelled")
                
            except Exception as e:
                logger.error(f"Analysis error for {ticker}: {str(e)}")
                st.error(f"Analysis failed: {str(e)}")
    
    elif ticker and not analyze_button:
        st.info("👆 Click 'Analyze' to get trading recommendations")


def show_portfolio_management():
    """Display portfolio management interface."""
    st.title("💼 Portfolio Management")
    
    pm = st.session_state.portfolio_manager
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "➕ Add/Edit Holdings", "🔧 Portfolio Settings"])
    
    with tab1:
        portfolio_name = st.session_state.selected_portfolio
        portfolio = pm.get_portfolio(portfolio_name)
        
        if portfolio:
            value_info = pm.get_portfolio_value(portfolio_name)
            holdings = pm.get_holdings(portfolio_name)
            
            st.subheader(f"Portfolio: {portfolio_name}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Value", format_currency(value_info['total_value']))
                st.metric("Cash Available", format_currency(value_info['cash_available']))
            
            with col2:
                st.metric("Holdings Value", format_currency(value_info['holdings_value']))
                st.metric("Trading Capital", format_currency(portfolio['trading_capital']))
            
            if holdings:
                st.markdown("---")
                st.subheader("Current Holdings")
                
                for holding in value_info['holdings_details']:
                    with st.expander(f"📈 {holding['symbol']} - {holding['quantity']} shares"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Avg Cost", format_currency(holding['avg_cost']))
                            st.metric("Market Value", format_currency(holding['market_value']))
                        
                        with col2:
                            st.metric("Current Price", format_currency(holding['current_price']))
                            st.metric("Unrealized P&L", format_currency(holding['unrealized_pnl']))
                        
                        with col3:
                            st.metric("P&L %", format_percentage(holding['unrealized_pnl_pct']))
                            
                            if st.button(f"Remove {holding['symbol']}", key=f"remove_{holding['symbol']}"):
                                pm.update_holding(portfolio_name, holding['symbol'], 0)
                                st.success(f"Removed {holding['symbol']}")
                                st.rerun()
        else:
            st.warning("Portfolio not found. Create one in Portfolio Settings.")
    
    with tab2:
        st.subheader("Add or Update Holdings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            symbol = st.text_input("Stock Symbol", key="add_symbol").upper()
        
        with col2:
            quantity = st.number_input("Quantity", min_value=0, value=0, step=1, key="add_quantity")
        
        with col3:
            avg_cost = st.number_input("Average Cost ($)", min_value=0.0, value=0.0, step=0.01, key="add_cost")
        
        if st.button("💾 Save Holding", type="primary"):
            if symbol and quantity > 0:
                try:
                    pm.update_holding(
                        st.session_state.selected_portfolio,
                        symbol,
                        quantity,
                        avg_cost if avg_cost > 0 else None
                    )
                    st.success(f"✅ Updated {quantity} shares of {symbol}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to update holding: {e}")
            else:
                st.warning("Please enter a valid symbol and quantity")
    
    with tab3:
        st.subheader("Portfolio Settings")
        
        # Create new portfolio
        with st.expander("➕ Create New Portfolio"):
            new_name = st.text_input("Portfolio Name", key="new_portfolio_name")
            new_capital = st.number_input(
                "Trading Capital ($)",
                min_value=0.0,
                value=5000.0,
                step=100.0,
                key="new_portfolio_capital"
            )
            
            if st.button("Create Portfolio", key="create_portfolio_btn"):
                if new_name:
                    try:
                        pm.create_portfolio(new_name, new_capital)
                        st.success(f"✅ Portfolio '{new_name}' created!")
                        st.session_state.selected_portfolio = new_name
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to create portfolio: {e}")
                else:
                    st.warning("Please enter a portfolio name")
        
        # Update trading capital
        portfolio = pm.get_portfolio(st.session_state.selected_portfolio)
        if portfolio:
            with st.expander("💰 Update Trading Capital"):
                current_capital = portfolio['trading_capital']
                st.write(f"Current capital: {format_currency(current_capital)}")
                
                new_capital = st.number_input(
                    "New Trading Capital ($)",
                    min_value=0.0,
                    value=current_capital,
                    step=100.0,
                    key="update_capital"
                )
                
                if st.button("Update Capital", key="update_capital_btn"):
                    if pm.update_trading_capital(st.session_state.selected_portfolio, new_capital):
                        st.success(f"✅ Updated capital to {format_currency(new_capital)}")
                        st.rerun()
                    else:
                        st.error("Failed to update capital")


def show_trade_history():
    """Display trade history."""
    st.title("📈 Trade History")
    
    pm = st.session_state.portfolio_manager
    portfolio_name = st.session_state.selected_portfolio
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        days = st.selectbox(
            "Time Period",
            [7, 30, 90, 180, 365],
            index=1,
            format_func=lambda x: f"Last {x} days"
        )
    
    # Get trades
    trades = pm.get_trade_history(portfolio_name, days)
    
    if not trades:
        st.info(f"No trades found in the last {days} days")
        return
    
    # Display summary
    col1, col2, col3, col4 = st.columns(4)
    
    buy_trades = [t for t in trades if t['action'] == 'BUY']
    sell_trades = [t for t in trades if t['action'] == 'SELL']
    total_volume = sum(abs(t['total_value']) for t in trades)
    
    with col1:
        st.metric("Total Trades", len(trades))
    
    with col2:
        st.metric("Buy Orders", len(buy_trades))
    
    with col3:
        st.metric("Sell Orders", len(sell_trades))
    
    with col4:
        st.metric("Total Volume", format_currency(total_volume))
    
    st.markdown("---")
    
    # Trade history table
    st.subheader("Trade Details")
    
    # Convert to DataFrame
    trade_data = []
    for trade in trades:
        # Safely format confidence
        confidence_value = trade.get('confidence')
        if confidence_value and isinstance(confidence_value, (int, float)):
            conf_display = f"{confidence_value*100:.0f}%"
        else:
            conf_display = 'N/A'
        
        trade_data.append({
            'Date': trade['timestamp'][:19],
            'Symbol': trade['symbol'],
            'Action': trade['action'],
            'Quantity': trade['quantity'],
            'Price': format_currency(trade['price']),
            'Total Value': format_currency(trade['total_value']),
            'Strategy': trade['strategy'] or 'Manual',
            'Confidence': conf_display
        })
    
    df = pd.DataFrame(trade_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Trade distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trades by Action")
        action_counts = pd.DataFrame(trades)['action'].value_counts()
        fig = px.pie(
            values=action_counts.values,
            names=action_counts.index,
            title="Buy vs Sell Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Trades by Strategy")
        strategies = [t['strategy'] or 'Manual' for t in trades]
        strategy_counts = pd.Series(strategies).value_counts()
        fig = px.bar(
            x=strategy_counts.index,
            y=strategy_counts.values,
            title="Trades per Strategy"
        )
        fig.update_layout(xaxis_title="Strategy", yaxis_title="Number of Trades")
        st.plotly_chart(fig, use_container_width=True)


def show_settings():
    """Display settings page."""
    st.title("⚙️ Settings")
    
    st.subheader("API Configuration")
    
    # Check API keys
    api_keys = st.session_state.api_keys
    
    st.info("API keys are loaded from the .env file. Do not share your keys!")
    
    # Display key status (masked)
    keys_to_check = [
        ('DISCORD_BOT_TOKEN', 'Discord Bot'),
        ('TWELVE_DATA_API_KEY', 'Twelve Data'),
        ('ALPHA_VANTAGE_API_KEY', 'Alpha Vantage'),
        ('NEWS_API_KEY', 'News API'),
        ('OPENAI_API_KEY', 'OpenAI')
    ]
    
    st.subheader("API Key Status")
    
    for key_name, display_name in keys_to_check:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**{display_name}:**")
        
        with col2:
            if api_keys.get(key_name):
                st.success("✅ Configured")
            else:
                st.error("❌ Missing")
    
    st.markdown("---")
    
    st.subheader("Application Settings")
    
    # Display environment settings
    trading_capital = api_keys.get('TRADING_CAPITAL', 5000.0)
    st.write(f"**Default Trading Capital:** ${trading_capital:,.2f}")
    
    min_pos = api_keys.get('MIN_POSITION_PERCENTAGE', 0.02)
    max_pos = api_keys.get('MAX_POSITION_PERCENTAGE', 0.10)
    st.write(f"**Position Size Range:** {min_pos*100:.0f}% - {max_pos*100:.0f}% of capital")
    
    st.markdown("---")
    
    st.subheader("About")
    st.write("""
    **AI Day Trader Agent - GUI Version**
    
    A sophisticated, multi-strategy AI-powered trading agent with an intuitive web interface.
    
    **Features:**
    - 📊 Real-time portfolio tracking
    - 🔍 Multi-strategy stock analysis
    - 💼 Portfolio management
    - 📈 Trade history and performance metrics
    - 🤖 AI-powered trading recommendations
    
    **Version:** 1.0.0
    
    For more information, visit the documentation or check the README.md file.
    """)


def main():
    """Main application entry point."""
    # Check for API key issues and show warning
    if hasattr(st.session_state, 'api_keys_error'):
        st.warning(
            "⚠️ Some API keys are not configured. "
            "Stock analysis features may be limited. "
            "Please set up your `.env` file with required API keys. "
            "See Settings for more details."
        )
    
    # Display sidebar and get selected page
    page = show_sidebar()
    
    # Route to appropriate page
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🔍 Stock Analysis":
        show_stock_analysis()
    elif page == "💼 Portfolio Management":
        show_portfolio_management()
    elif page == "📈 Trade History":
        show_trade_history()
    elif page == "⚙️ Settings":
        show_settings()


if __name__ == "__main__":
    main()
