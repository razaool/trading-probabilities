#!/usr/bin/env python3
"""Simple yfinance test"""

import yfinance as yf
import pandas as pd

print("=" * 60)
print("Testing yfinance")
print("=" * 60)
print(f"yfinance version: {yf.__version__}")
print()

# Test 1: Download function
print("Test 1: yf.download() for SPY (last 5 days)")
print("-" * 60)
try:
    data = yf.download('SPY', period='5d', progress=False)
    if not data.empty:
        print("✅ SUCCESS!")
        print(f"Retrieved {len(data)} days of data")
        print(data.head())
    else:
        print("❌ FAILED - Empty DataFrame")
except Exception as e:
    print(f"❌ FAILED - {e}")
    import traceback
    traceback.print_exc()

print()

# Test 2: Multiple tickers
print("Test 2: yf.download() for multiple tickers")
print("-" * 60)
try:
    data = yf.download('SPY AAPL MSFT', period='5d', progress=False)
    if not data.empty:
        print("✅ SUCCESS!")
        print(f"Shape: {data.shape}")
        print(f"Columns: {data.columns.tolist()}")
    else:
        print("❌ FAILED - Empty DataFrame")
except Exception as e:
    print(f"❌ FAILED - {e}")

print()

# Test 3: Different periods
print("Test 3: Different time periods")
print("-" * 60)
periods = ['1mo', '3mo', '6mo', '1y', '5y']
for period in periods:
    try:
        data = yf.download('SPY', period=period, progress=False)
        if not data.empty:
            print(f"  ✅ {period:5} - {len(data)} days")
        else:
            print(f"  ❌ {period:5} - Empty")
    except Exception as e:
        print(f"  ❌ {period:5} - Error: {e}")

print()
print("=" * 60)
