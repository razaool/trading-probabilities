"""
API route definitions
"""

from fastapi import APIRouter, HTTPException, Query as QueryParam
from typing import List
from app.models.schemas import QueryRequest, QueryResponse, TickerListResponse
from app.services.query_service import query_service
from app.services.constituents_service import constituents_service
from app.core.config import settings

router = APIRouter()


@router.get("/tickers", response_model=TickerListResponse)
async def get_available_tickers():
    """Get list of all available tickers"""
    return TickerListResponse(
        market_indices=settings.MARKET_INDICES,
        sector_etfs=settings.SECTOR_ETFs,
        volatility_indicators=settings.VOLATILITY_INDICATORS,
        sentiment_indicators=settings.SENTIMENT_INDICATORS,
        commodities=settings.COMMODITIES,
        top_stocks=settings.TOP_STOCKS,
    )


@router.post("/query", response_model=QueryResponse)
async def query_historical_patterns(query: QueryRequest):
    """
    Query historical patterns and get forward returns

    Examples:
    - NVDA declined 3% in a day: {"ticker": "NVDA", "condition_type": "percentage_change", "threshold": -3, "operator": "lt"}
    - VIX exceeded 30: {"ticker": "VIX", "condition_type": "absolute_threshold", "threshold": 30, "operator": "gt"}
    """
    try:
        result = await query_service.execute_query(query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@router.get("/tickers/suggest")
async def suggest_tickers(q: str = QueryParam(..., min_length=1, description="Search query")):
    """
    Get ticker suggestions based on search query

    Searches through cached ETF constituents and returns matching tickers with company names
    """
    try:
        suggestions = await constituents_service.search_tickers(q)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching suggestions: {str(e)}")


@router.get("/tickers/etf/{etf_ticker}")
async def get_etf_constituents(etf_ticker: str):
    """
    Get constituents for a specific ETF

    Returns the list of stocks held by the specified ETF
    """
    try:
        holdings = await constituents_service.get_etf_holdings(etf_ticker.upper())
        return {
            "etf": etf_ticker.upper(),
            "constituents": holdings,
            "count": len(holdings)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching constituents: {str(e)}")
