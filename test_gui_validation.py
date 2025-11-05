#!/usr/bin/env python3
"""
Quick validation test for GUI components.
Checks imports and basic functionality without running Streamlit.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        # Core modules
        from config.env_loader import load_env_variables
        print("  ✅ config.env_loader")
        
        from core.pipeline import EnhancedTradingPipeline
        print("  ✅ core.pipeline")
        
        from core.portfolio_manager import PortfolioManager
        print("  ✅ core.portfolio_manager")
        
        from utils.logger import get_logger
        print("  ✅ utils.logger")
        
        # Check if optional GUI dependencies would be needed
        try:
            import streamlit
            print("  ✅ streamlit (installed)")
        except ImportError:
            print("  ⚠️  streamlit (not installed - will be needed to run GUI)")
        
        try:
            import plotly
            print("  ✅ plotly (installed)")
        except ImportError:
            print("  ⚠️  plotly (not installed - will be needed to run GUI)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return False

def test_portfolio_manager():
    """Test basic PortfolioManager functionality."""
    print("\nTesting PortfolioManager...")
    
    try:
        from core.portfolio_manager import PortfolioManager
        pm = PortfolioManager()
        
        # Test basic operations
        portfolios = pm.list_portfolios()
        print(f"  ✅ Found {len(portfolios)} existing portfolios")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False

def test_gui_syntax():
    """Validate GUI app syntax."""
    print("\nValidating GUI app syntax...")
    
    try:
        import py_compile
        py_compile.compile('gui_app.py', doraise=True)
        print("  ✅ gui_app.py syntax valid")
        
        py_compile.compile('launch_gui.py', doraise=True)
        print("  ✅ launch_gui.py syntax valid")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Syntax validation failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("AI Day Trader Agent - GUI Validation Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Portfolio Manager", test_portfolio_manager()))
    results.append(("GUI Syntax", test_gui_syntax()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 All validation tests passed!")
        print("\nThe GUI is ready to use. Start it with:")
        print("  python launch_gui.py")
        print("  or")
        print("  streamlit run gui_app.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
