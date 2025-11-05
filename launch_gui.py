#!/usr/bin/env python3
"""
Simple launcher for the AI Day Trader Agent GUI.
Double-click this file or run: python launch_gui.py
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import streamlit
        import plotly
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing required dependencies...")
    print("This may take a few minutes...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed successfully!")

def main():
    """Main launcher function."""
    print("=" * 50)
    print("🚀 AI Day Trader Agent - GUI Launcher")
    print("=" * 50)
    print()
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("⚠️  Required dependencies not found.")
        install = input("Install now? (y/N): ").lower()
        
        if install == 'y':
            try:
                install_dependencies()
            except Exception as e:
                print(f"\n❌ Installation failed: {e}")
                print("\nPlease install manually:")
                print("  pip install -r requirements.txt")
                input("\nPress Enter to exit...")
                sys.exit(1)
        else:
            print("\n❌ Cannot start GUI without dependencies.")
            print("Please install manually:")
            print("  pip install -r requirements.txt")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    # Start the GUI
    print("\n🌐 Starting GUI...")
    print("The web interface will open at: http://localhost:8501")
    print("\n⚠️  To stop the server, press Ctrl+C in this window\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "gui_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 GUI stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting GUI: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
