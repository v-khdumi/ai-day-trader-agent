#!/bin/bash
# Startup script for AI Day Trader Agent GUI

echo "🚀 Starting AI Day Trader Agent GUI..."
echo "=========================================="
echo ""
echo "This will launch the web-based interface."
echo "Once started, open your browser to:"
echo "   👉 http://localhost:8501"
echo ""

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the Streamlit app
streamlit run gui_app.py --server.port 8501 --server.address localhost
