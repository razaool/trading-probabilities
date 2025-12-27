"""
Service for fetching and managing market data
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from app.core.config import settings


class DataService:
    """Service for fetching historical market data"""

    def __init__(self):
        self.cache = {}

    async def fetch_historical_data(
        self, ticker: str, period: str = "20y"
    ) -> pd.DataFrame:
        """
        Fetch historical data for a ticker

        Args:
            ticker: Ticker symbol
            period: Time period (e.g., "1y", "5y", "20y", "max")

        Returns:
            DataFrame with historical OHLCV data
        """
        if ticker in self.cache:
            cached_data, cached_time = self.cache[ticker]
            if datetime.now() - cached_time < timedelta(seconds=settings.DATA_CACHE_TTL):
                return cached_data

        try:
            data = yf.download(ticker, period=period, progress=False)
            self.cache[ticker] = (data, datetime.now())
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


data_service = DataService()
