"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date


class QueryRequest(BaseModel):
    """Request schema for historical pattern query"""

    ticker: str = Field(..., description="Ticker symbol to query")
    condition_type: Literal["percentage_change", "absolute_threshold"] = Field(
        ..., description="Type of condition"
    )
    threshold: float = Field(..., description="Threshold value")
    operator: Literal["gt", "lt", "gte", "lte", "eq"] = Field(
        ..., description="Comparison operator"
    )
    time_horizons: List[Literal["1d", "1w", "1m", "1y"]] = Field(
        default=["1d", "1w", "1m", "1y"], description="Forward time horizons to analyze"
    )


class PatternInstance(BaseModel):
    """Single instance where pattern occurred"""

    date: date
    forward_returns: dict[str, float]  # e.g., {"1d": 0.025, "1w": 0.031}


class QueryResponse(BaseModel):
    """Response schema for historical pattern query"""

    ticker: str
    condition: str
    reference_ticker: Optional[str] = None
    instances: List[PatternInstance]
    summary_statistics: dict[str, dict[str, float]]  # e.g., {"1d": {"mean": 0.02, ...}}
    total_occurrences: int


class TickerListResponse(BaseModel):
    """Response schema for available tickers"""

    market_indices: List[str]
    sector_etfs: List[str]
    volatility_indicators: List[str]
    sentiment_indicators: List[str]
    commodities: List[str]
    top_stocks: List[str]


class ErrorResponse(BaseModel):
    """Error response schema"""

    error: str
    detail: Optional[str] = None
