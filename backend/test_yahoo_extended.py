#!/usr/bin/env python3
"""Extended testing of Yahoo Finance fetcher"""

import sys
sys.path.insert(0, '/Users/razaool/trading-probabilities')

from app.services.yahoo_direct_fetcher import yahoo_fetcher

print("=" * 70)
print("EXTENDED YAHOO FINANCE API TESTING")
print("=" * 70)
print()

# Test different time periods
print("Test 1: Different Time Periods for SPY")
print("-" * 70)
periods = ["1mo", "3mo", "6mo", "1y", "5y", "max"]

for period in periods:
    data = yahoo_fetcher.fetch_data("SPY", period=period)
    if data is not None:
        print(f"  {period:6} - {len(data):4} records | {data.index[0].date()} to {data.index[-1].date()}")
    else:
        print(f"  {period:6} - FAILED")

print()

# Test multiple popular tickers
print("\nTest 2: Popular Tech Stocks (1 year)")
print("-" * 70)
tickers = [
    "SPY",   # S&P 500 ETF
    "QQQ",   # Nasdaq 100 ETF
    "NVDA",  # NVIDIA
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOGL", # Google
    "AMZN",  # Amazon
    "TSLA",  # Tesla
    "META",  # Meta
]

results = yahoo_fetcher.fetch_multiple(tickers, period="1y")

print(f"\n✅ Successfully fetched {len(results)}/{len(tickers)} tickers:")
for ticker, df in results.items():
    date_range = f"{df.index[0].date()} to {df.index[-1].date()}"
    price_range = f"${df['Close'].min():.2f} - ${df['Close'].max():.2f}"
    print(f"  {ticker:6} | {len(df):4} records | {date_range} | {price_range}")

print()

# Show detailed data for one ticker
print("\nTest 3: Detailed Data for NVDA (3 months)")
print("-" * 70)
nvda = yahoo_fetcher.fetch_data("NVDA", period="3mo")
if nvda is not None:
    print(f"\nTotal records: {len(nvda)}")
    print(f"Date range: {nvda.index[0].date()} to {nvda.index[-1].date()}")
    print(f"\nFirst 5 days:")
    print(nvda.head())
    print(f"\nLast 5 days:")
    print(nvda.tail())

    # Calculate some stats
    daily_returns = nvda['Close'].pct_change() * 100
    print(f"\nStatistics:")
    print(f"  Average daily return: {daily_returns.mean():.2f}%")
    print(f"  Best day: {daily_returns.max():.2f}%")
    print(f"  Worst day: {daily_returns.min():.2f}%")
    print(f"  Total return: {((nvda['Close'].iloc[-1] / nvda['Close'].iloc[0] - 1) * 100):.2f}%")

print()
print("=" * 70)
