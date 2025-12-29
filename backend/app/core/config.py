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
    # For production, ALWAYS override this via environment variable
    # Format: comma-separated URLs or ["http://example.com", "https://example.com"]
    # To allow all origins (NOT recommended for production): CORS_ORIGINS=["*"]
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://192.168.1.66:5173",
        "http://192.168.1.66:5174",
        "https://trading-probabilities.vercel.app",  # Production Vercel URL
    ]

    # Allow all origins for development/previews (set via environment variable)
    CORS_ALLOW_ALL: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./data/trading_patterns.db"

    # Data fetching
    DATA_CACHE_ENABLED: bool = True
    DATA_CACHE_TTL: int = 86400  # 24 hours in seconds

    # Supported tickers
    MARKET_INDICES: List[str] = ["SPY", "QQQ", "DIA"]
    SECTOR_ETFs: List[str] = ["XLF", "XLE", "XLK", "XLV", "XLY", "XLP"]
    VOLATILITY_INDICATORS: List[str] = ["VIX", "^VIX", "VXN", "^VXN"]
    SENTIMENT_INDICATORS: List[str] = ["PCR"]
    COMMODITIES: List[str] = ["GLD", "USO", "SLV"]

    # Top stocks - fetched dynamically from index holdings or external APIs
    # For now, users can query any ticker symbol directly
    TOP_STOCKS: List[str] = []  # Empty list - any ticker can be queried

    # Indicator mappings (indicator -> reference asset)
    INDICATOR_REFERENCES: dict = {
        "VIX": "SPY",
        "^VIX": "SPY",
        "VXN": "QQQ",
        "^VXN": "QQQ",
        "PCR": "SPY",
    }

    # Security
    API_KEYS: List[str] = []  # Empty means no auth required (dev mode)
    REQUIRE_AUTH: bool = False  # Can be enabled via environment variable

    # Rate Limiting
    ENABLE_RATE_LIMIT: bool = True
    RATE_LIMIT_PER_MINUTE: int = 10  # Requests per minute per IP
    RATE_LIMIT_BURST: int = 20  # Burst size

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
