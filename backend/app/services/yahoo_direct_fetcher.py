"""
Direct Yahoo Finance API fetcher that bypasses yfinance library
Uses the official Yahoo Finance API v8 endpoint
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, List


class YahooFinanceFetcher:
    """Fetch data directly from Yahoo Finance API v8"""

    def __init__(self):
        self.base_url = "https://query2.finance.yahoo.com/v8/finance/chart/"
        self.session = requests.Session()
        # Use Windows User-Agent to avoid rate limiting
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def fetch_data(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Fetch historical data for a symbol

        Args:
            symbol: Stock/ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max)
            interval: Data interval (1d, 1wk, 1mo)

        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = self._calculate_start_date(period)

            # Build request parameters
            params = {
                "period1": int(start_date.timestamp()),
                "period2": int(end_date.timestamp()),
                "interval": interval,
                "includePrePost": True,
            }

            # Make request
            url = f"{self.base_url}{symbol}"
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"  ❌ HTTP {response.status_code} for {symbol}")
                return None

            # Parse JSON response
            data = response.json()
            result = data.get("chart", {}).get("result", [])

            if not result:
                print(f"  ❌ No data returned for {symbol}")
                return None

            # Extract data
            meta = result[0].get("meta", {})
            timestamps = result[0].get("timestamp", [])
            indicators = result[0].get("indicators", {})
            quote = indicators.get("quote", [{}])[0]

            if not timestamps:
                print(f"  ❌ No timestamps in response for {symbol}")
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

            # Add Adj Close (same as Close for simplicity)
            df["Adj Close"] = df["Close"]

            print(f"  ✅ Fetched {len(df)} records for {symbol}")

            return df

        except Exception as e:
            print(f"  ❌ Error fetching {symbol}: {e}")
            return None

    def fetch_multiple(
        self,
        symbols: List[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> dict:
        """
        Fetch data for multiple symbols

        Args:
            symbols: List of ticker symbols
            period: Time period
            interval: Data interval

        Returns:
            Dictionary mapping symbol to DataFrame
        """
        results = {}

        for symbol in symbols:
            data = self.fetch_data(symbol, period, interval)
            if data is not None:
                results[symbol] = data

        return results

    def _calculate_start_date(self, period: str) -> datetime:
        """Calculate start date from period string"""
        now = datetime.now()

        period_map = {
            "1d": timedelta(days=1),
            "5d": timedelta(days=5),
            "1mo": timedelta(days=30),
            "3mo": timedelta(days=90),
            "6mo": timedelta(days=180),
            "1y": timedelta(days=365),
            "5y": timedelta(days=365*5),
            "max": timedelta(days=365*50),  # 50 years
        }

        if period in period_map:
            return now - period_map[period]
        else:
            return now - timedelta(days=365)  # Default to 1 year


# Create singleton instance
yahoo_fetcher = YahooFinanceFetcher()


if __name__ == "__main__":
    # Test the fetcher
    print("=" * 60)
    print("Testing Direct Yahoo Finance API Fetcher")
    print("=" * 60)
    print()

    # Test single ticker
    print("Test 1: SPY (1 month)")
    print("-" * 60)
    fetcher = YahooFinanceFetcher()
    data = fetcher.fetch_data("SPY", period="1mo")

    if data is not None:
        print(f"\nShape: {data.shape}")
        print(f"\nFirst 5 rows:")
        print(data.head())
        print(f"\nLast 5 rows:")
        print(data.tail())

    print()

    # Test multiple tickers
    print("\nTest 2: Multiple tickers (1 week)")
    print("-" * 60)
    symbols = ["SPY", "QQQ", "NVDA", "AAPL", "MSFT"]
    results = fetcher.fetch_multiple(symbols, period="5d")

    print(f"\n✅ Successfully fetched {len(results)}/{len(symbols)} tickers:")
    for symbol, df in results.items():
        print(f"  {symbol}: {len(df)} records")

    print()
    print("=" * 60)
