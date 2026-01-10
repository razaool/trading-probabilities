#!/usr/bin/env python3
"""
Update market data for all tickers in the database.

This script fetches the latest trading data from Yahoo Finance for all tickers
and updates the PostgreSQL database with new price records and daily returns.

Run this script weekly (e.g., every Saturday) to keep the database current.
"""

import os
import sys
import time
import random
from datetime import datetime, timedelta, date
from typing import List, Tuple, Dict, Optional
import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
import requests
from tqdm import tqdm
from sqlalchemy import create_engine, text


class YahooFinanceFetcher:
    """Fetch data directly from Yahoo Finance API v8 (Python 3.9 compatible)"""

    def __init__(self):
        self.base_url = "https://query2.finance.yahoo.com/v8/finance/chart/"
        self.session = requests.Session()
        # Use Windows User-Agent to avoid rate limiting
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_data(self, symbol: str, start_date: date, end_date: date) -> Optional[pd.DataFrame]:
        """
        Fetch historical data for a symbol within a date range.

        Args:
            symbol: Stock/ticker symbol
            start_date: Start date (inclusive)
            end_date: End date (inclusive)

        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            # Convert date to datetime for timestamp calculation
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())

            # Build request parameters
            params = {
                "period1": int(start_datetime.timestamp()),
                "period2": int((end_datetime + timedelta(days=1)).timestamp()),  # +1 to include end_date
                "interval": "1d",
                "includePrePost": True,
            }

            # Make request
            url = f"{self.base_url}{symbol}"
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code != 200:
                return None

            # Parse JSON response
            data = response.json()
            result = data.get("chart", {}).get("result", [])

            if not result:
                return None

            # Extract data
            timestamps = result[0].get("timestamp", [])
            indicators = result[0].get("indicators", {})
            quote = indicators.get("quote", [{}])[0]

            if not timestamps:
                return None

            # Build DataFrame
            df_data = {
                "Date": [datetime.fromtimestamp(ts) for ts in timestamps],
                "Open": quote.get("open", []),
                "High": quote.get("high", []),
                "Low": quote.get("low", []),
                "Close": quote.get("close", []),
                "Volume": quote.get("volume", []),
            }

            # Create DataFrame
            df = pd.DataFrame(df_data)
            df.set_index("Date", inplace=True)

            # Remove any rows with missing data
            df.dropna(inplace=True)

            # Convert to proper types
            for col in ["Open", "High", "Low", "Close"]:
                df[col] = df[col].astype(float)
            df["Volume"] = df["Volume"].astype(int)

            # Add Adj Close (same as Close)
            df["Adj Close"] = df["Close"]

            return df

        except Exception as e:
            return None


def get_database_url() -> str:
    """Get database URL from environment or use default"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)
    return db_url


def get_all_tickers(conn) -> List[str]:
    """Get all ticker symbols from database"""
    with conn.cursor() as cur:
        cur.execute("SELECT symbol FROM tickers ORDER BY symbol;")
        tickers = [row[0] for row in cur.fetchall()]
    return tickers


def get_ticker_latest_date(conn, ticker: str) -> Optional[date]:
    """Get the latest date for a ticker from historical_prices"""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT MAX(date) FROM historical_prices WHERE ticker = %s;",
            (ticker,)
        )
        result = cur.fetchone()
        return result[0] if result and result[0] else None


def fetch_yahoo_data(fetcher: YahooFinanceFetcher, ticker: str, start_date: date, end_date: date) -> Optional[pd.DataFrame]:
    """
    Fetch data from Yahoo Finance for a specific date range.

    Args:
        fetcher: YahooFinanceFetcher instance
        ticker: Ticker symbol
        start_date: Start date (inclusive)
        end_date: End date (inclusive)

    Returns:
        DataFrame with OHLCV data or None if failed
    """
    try:
        # Add a small delay to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))

        # Fetch data using direct Yahoo API
        data = fetcher.fetch_data(ticker, start_date, end_date)

        if data is None or data.empty:
            return None

        return data

    except Exception as e:
        print(f"  ❌ Error fetching {ticker}: {str(e)}")
        return None


def prepare_price_data(ticker: str, data: pd.DataFrame) -> List[Tuple]:
    """
    Prepare price data for batch insertion.

    Returns:
        List of tuples: (ticker, date, open, high, low, close, volume, adjusted_close)
    """
    records = []

    for idx in data.index:
        date = idx.strftime('%Y-%m-%d')

        # Handle volume - cap at BIGINT max if needed
        volume_val = data['Volume'].loc[idx]
        if pd.isna(volume_val):
            volume_int = None
        elif volume_val > 9223372036854775807:  # BIGINT max
            volume_int = 9223372036854775807
        else:
            volume_int = int(volume_val)

        # Use 'Adj Close' if available, otherwise use 'Close'
        adj_close = float(data['Adj Close'].loc[idx]) if 'Adj Close' in data.columns else float(data['Close'].loc[idx])

        record = (
            ticker,
            date,
            float(data['Open'].loc[idx]),
            float(data['High'].loc[idx]),
            float(data['Low'].loc[idx]),
            float(data['Close'].loc[idx]),
            volume_int,
            adj_close
        )
        records.append(record)

    return records


def calculate_daily_returns(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily percentage returns from price data"""
    data_copy = data.copy()
    data_copy['daily_return'] = data_copy['Close'].pct_change() * 100
    return data_copy


def prepare_return_data(ticker: str, data_with_returns: pd.DataFrame) -> List[Tuple]:
    """
    Prepare return data for batch insertion.

    Returns:
        List of tuples: (ticker, date, return_pct)
    """
    records = []

    for idx in data_with_returns.index:
        daily_ret = data_with_returns['daily_return'].loc[idx]

        # Skip NaN returns (first day)
        import numpy as np
        if pd.isna(daily_ret) or np.isnan(daily_ret):
            continue

        record = (
            ticker,
            idx.strftime('%Y-%m-%d'),
            float(daily_ret)
        )
        records.append(record)

    return records


def update_ticker_metadata(conn, ticker: str, data: pd.DataFrame):
    """Update ticker metadata (latest_date, last_updated)"""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE tickers
            SET
                latest_date = %s,
                last_updated = %s
            WHERE symbol = %s;
            """,
            (
                data.index[-1].strftime('%Y-%m-%d'),
                datetime.now().strftime('%Y-%m-%d'),
                ticker
            )
        )


def update_ticker(conn, fetcher: YahooFinanceFetcher, ticker: str, start_date: date, end_date: date) -> Dict[str, int]:
    """
    Update a single ticker with new data.

    Returns:
        Dictionary with counts: {'prices_added': int, 'returns_added': int, 'error': bool}
    """
    result = {'prices_added': 0, 'returns_added': 0, 'error': False}

    # Fetch data from Yahoo Finance
    data = fetch_yahoo_data(fetcher, ticker, start_date, end_date)
    if data is None:
        result['error'] = True
        return result

    # Filter to only new dates (in case Yahoo returns some old data)
    latest_in_db = get_ticker_latest_date(conn, ticker)
    if latest_in_db:
        data = data[data.index > pd.Timestamp(latest_in_db)]

    if data.empty:
        return result

    # Prepare and insert price data
    price_records = prepare_price_data(ticker, data)

    with conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO historical_prices
            (ticker, date, open, high, low, close, volume, adjusted_close)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticker, date) DO NOTHING
            """,
            price_records,
            page_size=1000
        )
        result['prices_added'] = len(price_records)

    # Calculate and insert returns
    data_with_returns = calculate_daily_returns(data)
    return_records = prepare_return_data(ticker, data_with_returns)

    with conn.cursor() as cur:
        execute_batch(
            cur,
            """
            INSERT INTO daily_returns (ticker, date, return_pct)
            VALUES (%s, %s, %s)
            ON CONFLICT (ticker, date) DO UPDATE SET
                return_pct = EXCLUDED.return_pct
            """,
            return_records,
            page_size=1000
        )
        result['returns_added'] = len(return_records)

    # Update ticker metadata
    update_ticker_metadata(conn, ticker, data)

    conn.commit()

    return result


def main():
    """Main update process"""
    print("=" * 70)
    print("Market Data Update Script")
    print("=" * 70)
    print()

    # Get database connection
    db_url = get_database_url()
    print(f"📡 Connecting to database...")

    try:
        conn = psycopg2.connect(db_url)
        print(f"✅ Connected to database")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        sys.exit(1)

    # Create Yahoo Finance fetcher
    fetcher = YahooFinanceFetcher()

    # Get all tickers
    print(f"📋 Fetching ticker list...")
    tickers = get_all_tickers(conn)
    print(f"✅ Found {len(tickers)} tickers")
    print()

    # Calculate date range
    end_date = datetime.now().date() - timedelta(days=1)  # Yesterday
    print(f"📅 End date: {end_date}")
    print()

    # Statistics
    total_prices_added = 0
    total_returns_added = 0
    failed_tickers = []

    # Process each ticker
    print(f"🔄 Processing tickers...")
    print()

    for ticker in tqdm(tickers, desc="Updating tickers"):
        # Get latest date for this ticker
        latest_date = get_ticker_latest_date(conn, ticker)

        if latest_date is None:
            print(f"  ⚠️  {ticker}: No existing data, skipping")
            failed_tickers.append(ticker)
            continue

        # Calculate start date (day after latest)
        start_date = latest_date + timedelta(days=1)

        # Check if update is needed
        if start_date > end_date:
            # Data is already current
            continue

        # Update this ticker
        try:
            result = update_ticker(conn, fetcher, ticker, start_date, end_date)

            if result['error']:
                failed_tickers.append(ticker)
            else:
                total_prices_added += result['prices_added']
                total_returns_added += result['returns_added']

        except Exception as e:
            print(f"  ❌ Error updating {ticker}: {str(e)}")
            failed_tickers.append(ticker)

    # Close connection
    conn.close()

    # Print summary
    print()
    print("=" * 70)
    print("UPDATE SUMMARY")
    print("=" * 70)
    print(f"✅ Price records added: {total_prices_added:,}")
    print(f"✅ Return records added: {total_returns_added:,}")
    print(f"📊 Tickers processed: {len(tickers)}")
    print(f"❌ Failed tickers: {len(failed_tickers)}")

    if failed_tickers:
        print()
        print("Failed tickers:")
        for ticker in failed_tickers[:10]:  # Show first 10
            print(f"  - {ticker}")
        if len(failed_tickers) > 10:
            print(f"  ... and {len(failed_tickers) - 10} more")

    print()
    print(f"✅ Update completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


if __name__ == "__main__":
    main()
