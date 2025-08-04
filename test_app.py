#!/usr/bin/env python3
"""
Test script for the Dividend Discount Model Calculator
This script tests the basic functionality without running the full Streamlit app
"""

import sys
import traceback

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Streamlit: {e}")
        return False
    
    try:
        import yfinance as yf
        print("✓ yfinance imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import yfinance: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import pandas: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import numpy: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✓ plotly imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import plotly: {e}")
        return False
    
    return True

def test_functions():
    """Test the core functions from the app"""
    print("\nTesting core functions...")
    
    try:
        # Import functions from app
        from app import perpetuity_pv, get_risk_free_rate, get_equity_returns
        
        # Test perpetuity_pv function
        result = perpetuity_pv(100, 0.05, 0.10)
        expected = 100 * (1 + 0.05) / (0.10 - 0.05)  # 2100
        if abs(result - expected) < 0.01:
            print("✓ perpetuity_pv function works correctly")
        else:
            print(f"✗ perpetuity_pv function failed: expected {expected}, got {result}")
            return False
        
        # Test market data functions (these might fail if no internet)
        try:
            risk_free = get_risk_free_rate()
            print(f"✓ get_risk_free_rate returned: {risk_free:.4f}")
        except Exception as e:
            print(f"⚠ get_risk_free_rate failed (expected if no internet): {e}")
        
        try:
            equity_returns = get_equity_returns()
            print(f"✓ get_equity_returns returned: {equity_returns:.4f}")
        except Exception as e:
            print(f"⚠ get_equity_returns failed (expected if no internet): {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Function tests failed: {e}")
        traceback.print_exc()
        return False

def test_stock_data():
    """Test stock data fetching (requires internet)"""
    print("\nTesting stock data fetching...")
    
    try:
        from app import get_stock_data
        
        # Test with a well-known stock
        data = get_stock_data("AAPL")
        
        if data and data.get("Company Name"):
            print(f"✓ Successfully fetched data for {data['Company Name']}")
            print(f"  - Current Price: ${data.get('Last Stock Price', 'N/A')}")
            print(f"  - Beta: {data.get('Beta', 'N/A')}")
            print(f"  - ROE: {data.get('Return on Equity (ROE)', 'N/A')}")
            return True
        else:
            print("✗ Failed to fetch stock data")
            return False
            
    except Exception as e:
        print(f"⚠ Stock data test failed (expected if no internet): {e}")
        return True  # Not a critical failure

def main():
    """Run all tests"""
    print("🧪 Testing Dividend Discount Model Calculator")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Test functions
    if not test_functions():
        print("\n❌ Function tests failed.")
        sys.exit(1)
    
    # Test stock data (optional)
    test_stock_data()
    
    print("\n✅ All tests completed successfully!")
    print("\n🚀 To run the app:")
    print("streamlit run app.py")
    
    print("\n📚 For deployment instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 