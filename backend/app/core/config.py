"""
Application configuration
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Historical Pattern Analysis Tool"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./data/trading_patterns.db"

    # Data fetching
    DATA_CACHE_ENABLED: bool = True
    DATA_CACHE_TTL: int = 86400  # 24 hours in seconds

    # Supported tickers
    MARKET_INDICES: List[str] = ["SPY", "QQQ", "DIA", "IWM"]
    SECTOR_ETFs: List[str] = ["XLF", "XLE", "XLK", "XLV", "XLY", "XLP"]
    VOLATILITY_INDICATORS: List[str] = ["VIX", "VXN", "RVX"]
    SENTIMENT_INDICATORS: List[str] = ["PUT_CALL_RATIO"]
    COMMODITIES: List[str] = ["GLD", "USO", "SLV"]

    # Top stocks - fetched dynamically from index holdings or external APIs
    # For now, users can query any ticker symbol directly
    TOP_STOCKS: List[str] = []  # Empty list - any ticker can be queried

    # Indicator mappings (indicator -> reference asset)
    INDICATOR_REFERENCES: dict = {
        "VIX": "SPY",
        "VXN": "QQQ",
        "RVX": "IWM",
        "PUT_CALL_RATIO": "SPY",
    }

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
