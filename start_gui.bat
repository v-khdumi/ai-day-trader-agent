@echo off
REM Startup script for AI Day Trader Agent GUI (Windows)

echo.
echo ========================================
echo   AI Day Trader Agent GUI
echo ========================================
echo.
echo Starting the web-based interface...
echo Once started, open your browser to:
echo    http://localhost:8501
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Start the Streamlit app
streamlit run gui_app.py --server.port 8501 --server.address localhost
