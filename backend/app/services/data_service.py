"""
Service for fetching and managing market data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import create_engine, text
from app.core.config import settings


class DataService:
    """Service for fetching historical market data"""

    def __init__(self):
        self.cache = {}  # In-memory cache (fallback)
        self.db_engine = create_engine(settings.DATABASE_URL)

    async def fetch_historical_data(
        self, ticker: str, period: str = "20y"
    ) -> pd.DataFrame:
        """
        Fetch historical data for a ticker
        - First tries database (fast)
        - Falls back to yfinance if not in DB (slow, then caches to DB)

        Args:
            ticker: Ticker symbol
            period: Time period (e.g., "1y", "5y", "20y", "max")

        Returns:
            DataFrame with historical OHLCV data
        """
        # Step 1: Try to get from database first
        db_data = self._get_from_database(ticker)
        if db_data is not None:
            print(f"✅ Retrieved {ticker} from database")
            return db_data

        # Step 2: Not in DB - fetch from yfinance and store
        print(f"⚠️  {ticker} not in database, fetching from yfinance...")
        try:
            # Download with auto_adjust=False to get Adj Close column
            data = yf.download(ticker, period=period, progress=False, auto_adjust=False)
            if data.empty:
                raise ValueError(f"No data available for {ticker}")

            # Store in database for next time
            self._save_to_database(ticker, data)
            print(f"✅ Cached {ticker} to database")
            return data

        except Exception as e:
            raise ValueError(f"Failed to fetch data for {ticker}: {str(e)}")

    async def fetch_multiple_tickers(
        self, tickers: List[str], period: str = "20y"
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical data for multiple tickers

        Args:
            tickers: List of ticker symbols
            period: Time period

        Returns:
            Dictionary mapping ticker to DataFrame
        """
        results = {}
        for ticker in tickers:
            try:
                data = await self.fetch_historical_data(ticker, period)
                results[ticker] = data
            except Exception as e:
                print(f"Warning: Failed to fetch {ticker}: {str(e)}")
        return results

    def calculate_percentage_change(
        self, data: pd.DataFrame
    ) -> pd.Series:
        """
        Calculate daily percentage changes

        Args:
            data: DataFrame with 'Close' prices

        Returns:
            Series of daily percentage changes
        """
        return data["Close"].pct_change() * 100

    def get_forward_returns(
        self,
        data: pd.DataFrame,
        start_date: datetime,
        horizons: Dict[str, int] = None,
    ) -> Dict[str, float]:
        """
        Calculate forward returns from a given date

        Args:
            data: DataFrame with historical prices
            start_date: Date to calculate from
            horizons: Dictionary mapping horizon names to days (e.g., {"1d": 1, "1w": 5})

        Returns:
            Dictionary of forward returns
        """
        if horizons is None:
            horizons = {"1d": 1, "1w": 5, "1m": 21, "1y": 252}

        returns = {}
        start_price = data.loc[start_date, "Close"]

        for horizon_name, days in horizons.items():
            try:
                # Find the closest future date
                future_idx = data.index.get_loc(start_date) + days
                if future_idx < len(data):
                    future_price = data.iloc[future_idx]["Close"]
                    returns[horizon_name] = (
                        (future_price - start_price) / start_price
                    ) * 100
                else:
                    returns[horizon_name] = None
            except (KeyError, IndexError):
                returns[horizon_name] = None

        return returns

    def is_indicator(self, ticker: str) -> bool:
        """Check if a ticker is an indicator"""
        return ticker in settings.INDICATOR_REFERENCES

    def get_reference_ticker(self, indicator: str) -> Optional[str]:
        """Get the reference ticker for an indicator"""
        return settings.INDICATOR_REFERENCES.get(indicator)

    def _get_from_database(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Load ticker data from database (SQLite or PostgreSQL)

        Args:
            ticker: Ticker symbol

        Returns:
            DataFrame with OHLCV data or None if not found
        """
        try:
            # Detect database type from URL
            is_postgresql = settings.DATABASE_URL.startswith("postgresql")

            # Query historical prices from database
            # Use different parameter syntax for PostgreSQL vs SQLite
            if is_postgresql:
                query = """
                    SELECT date, open, high, low, close, volume, adjusted_close
                    FROM historical_prices
                    WHERE ticker = %s
                    ORDER BY date
                """
                df = pd.read_sql(query, self.db_engine, params=(ticker,))
            else:
                query = """
                    SELECT date, open, high, low, close, volume, adjusted_close
                    FROM historical_prices
                    WHERE ticker = ?
                    ORDER BY date
                """
                df = pd.read_sql(query, self.db_engine, params=(ticker,))

            if df.empty:
                return None

            # Convert to DataFrame format expected by the rest of the app
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            df.index.name = 'Date'  # Match yfinance format

            # Rename columns to match yfinance format (capital first letter)
            df.rename(columns={
                'adjusted_close': 'Adj Close',
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            }, inplace=True)

            return df

        except Exception as e:
            print(f"Error reading from database: {e}")
            return None

    def _save_to_database(self, ticker: str, data: pd.DataFrame) -> bool:
        """
        Save ticker data to database (SQLite or PostgreSQL)

        Args:
            ticker: Ticker symbol
            data: DataFrame with OHLCV data

        Returns:
            True if successful, False otherwise
        """
        try:
            # Detect database type from URL
            is_postgresql = settings.DATABASE_URL.startswith("postgresql")

            # Calculate daily returns
            data_copy = data.copy()
            data_copy['daily_return'] = data_copy['Close'].pct_change() * 100

            # Use connection context manager for SQLAlchemy 2.0+
            with self.db_engine.connect() as conn:
                # Check if 'Adj Close' column exists, otherwise use 'Close'
                adj_close_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'

                # Insert price data using direct column access
                for idx in range(len(data)):
                    date = data.index[idx]
                    volume_val = data['Volume'].iloc[idx]
                    # Handle large volume values - use None if too large or NaN
                    volume_int = None if pd.isna(volume_val) or volume_val > 2147483647 else int(volume_val)

                    if is_postgresql:
                        # PostgreSQL uses ON CONFLICT instead of INSERT OR REPLACE
                        conn.execute(
                            text("""
                                INSERT INTO historical_prices
                                (ticker, date, open, high, low, close, volume, adjusted_close)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (ticker, date) DO UPDATE SET
                                    open = EXCLUDED.open,
                                    high = EXCLUDED.high,
                                    low = EXCLUDED.low,
                                    close = EXCLUDED.close,
                                    volume = EXCLUDED.volume,
                                    adjusted_close = EXCLUDED.adjusted_close
                            """),
                            (
                                ticker,
                                date.strftime('%Y-%m-%d'),
                                float(data['Open'].iloc[idx]),
                                float(data['High'].iloc[idx]),
                                float(data['Low'].iloc[idx]),
                                float(data['Close'].iloc[idx]),
                                volume_int,
                                float(data[adj_close_col].iloc[idx])
                            )
                        )
                    else:
                        # SQLite uses INSERT OR REPLACE
                        conn.execute(
                            text("""
                                INSERT OR REPLACE INTO historical_prices
                                (ticker, date, open, high, low, close, volume, adjusted_close)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """),
                            (
                                ticker,
                                date.strftime('%Y-%m-%d'),
                                float(data['Open'].iloc[idx]),
                                float(data['High'].iloc[idx]),
                                float(data['Low'].iloc[idx]),
                                float(data['Close'].iloc[idx]),
                                volume_int,
                                float(data[adj_close_col].iloc[idx])
                            )
                        )

                # Insert daily returns
                for idx in range(len(data_copy)):
                    daily_ret = data_copy['daily_return'].iloc[idx]
                    # Check if not NaN using numpy's isnan which handles scalars properly
                    import numpy as np
                    if not isinstance(daily_ret, float) or not np.isnan(daily_ret):
                        if is_postgresql:
                            conn.execute(
                                text("""
                                    INSERT INTO daily_returns (ticker, date, return_pct)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (ticker, date) DO UPDATE SET
                                        return_pct = EXCLUDED.return_pct
                                """),
                                (
                                    ticker,
                                    data_copy.index[idx].strftime('%Y-%m-%d'),
                                    float(daily_ret)
                                )
                            )
                        else:
                            conn.execute(
                                text("""
                                    INSERT OR REPLACE INTO daily_returns (ticker, date, return_pct)
                                    VALUES (?, ?, ?)
                                """),
                                (
                                    ticker,
                                    data_copy.index[idx].strftime('%Y-%m-%d'),
                                    float(daily_ret)
                                )
                            )

                # Update ticker metadata
                if is_postgresql:
                    conn.execute(
                        text("""
                            INSERT INTO tickers
                            (symbol, name, type, data_available, earliest_date, latest_date, last_updated)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (symbol) DO UPDATE SET
                                name = EXCLUDED.name,
                                type = EXCLUDED.type,
                                data_available = EXCLUDED.data_available,
                                earliest_date = EXCLUDED.earliest_date,
                                latest_date = EXCLUDED.latest_date,
                                last_updated = EXCLUDED.last_updated
                        """),
                        (
                            ticker,
                            ticker,
                            'stock',
                            True,
                            data.index[0].strftime('%Y-%m-%d'),
                            data.index[-1].strftime('%Y-%m-%d'),
                            datetime.now().strftime('%Y-%m-%d')
                        )
                    )
                else:
                    conn.execute(
                        text("""
                            INSERT OR REPLACE INTO tickers
                            (symbol, name, type, data_available, earliest_date, latest_date, last_updated)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """),
                        (
                            ticker,
                            ticker,
                            'stock',
                            True,
                            data.index[0].strftime('%Y-%m-%d'),
                            data.index[-1].strftime('%Y-%m-%d'),
                            datetime.now().strftime('%Y-%m-%d')
                        )
                    )

                # Commit the transaction
                conn.commit()

            return True

        except Exception as e:
            print(f"Error saving to database: {e}")
            import traceback
            traceback.print_exc()
            return False


data_service = DataService()
