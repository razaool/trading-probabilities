"""
Service for fetching market data from Yahoo Finance with proper headers
"""

import yfinance as yf
import pandas as pd
import requests
from typing import Optional


def create_yfinance_session():
    """
    Create a requests session with headers that avoid Yahoo Finance rate limiting
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session


def fetch_ticker_data(ticker: str, period: str = "1y") -> Optional[pd.DataFrame]:
    """
    Fetch historical data for a ticker using yfinance with proper headers

    Args:
        ticker: Ticker symbol
        period: Time period (e.g., "1mo", "3mo", "6mo", "1y", "5y", "max")

    Returns:
        DataFrame with OHLCV data or None if failed
    """
    try:
        # Create session with proper headers
        session = create_yfinance_session()

        # Fetch data using yfinance with custom session
        data = yf.download(
            ticker,
            period=period,
            progress=False,
            session=session
        )

        if data.empty:
            print(f"  ⚠️  No data returned for {ticker}")
            return None

        print(f"  ✅ Fetched {len(data)} records for {ticker}")
        return data

    except Exception as e:
        print(f"  ❌ Error fetching {ticker}: {e}")
        return None


def fetch_multiple_tickers(tickers: list, period: str = "1y") -> dict:
    """
    Fetch historical data for multiple tickers

    Args:
        tickers: List of ticker symbols
        period: Time period

    Returns:
        Dictionary mapping ticker to DataFrame
    """
    results = {}

    print(f"Fetching data for {len(tickers)} tickers (period: {period})...")
    print()

    for ticker in tickers:
        data = fetch_ticker_data(ticker, period)
        if data is not None:
            results[ticker] = data

    print()
    print(f"✅ Successfully fetched {len(results)}/{len(tickers)} tickers")

    return results


if __name__ == "__main__":
    # Test the fetcher
    print("=" * 60)
    print("Testing yfinance with proper headers")
    print("=" * 60)
    print()

    # Test single ticker
    print("Test 1: Single ticker (SPY, 1 month)")
    print("-" * 60)
    data = fetch_ticker_data("SPY", period="1mo")
    if data is not None:
        print(f"\nShape: {data.shape}")
        print(f"Columns: {data.columns.tolist()}")
        print(f"\nFirst 3 rows:")
        print(data.head(3))
        print(f"\nLast 3 rows:")
        print(data.tail(3))

    print()

    # Test multiple tickers
    print("\nTest 2: Multiple tickers (SPY, QQQ, NVDA, 1 week)")
    print("-" * 60)
    tickers = ["SPY", "QQQ", "NVDA"]
    results = fetch_multiple_tickers(tickers, period="1wk")

    for ticker, data in results.items():
        print(f"{ticker}: {len(data)} records")

    print()
    print("=" * 60)
