"""
API route definitions
"""

from fastapi import APIRouter, HTTPException, Query as QueryParam, Depends, Request
from typing import List
from app.models.schemas import QueryRequest, QueryResponse, TickerListResponse
from app.services.query_service import query_service
from app.services.constituents_service import constituents_service
from app.core.config import settings
from app.core.security import verify_api_key
from app.core.rate_limit import limiter

router = APIRouter()

# Authentication dependency - can be enabled via REQUIRE_AUTH env var
auth_required = Depends(verify_api_key)

# Rate limiting decorator (conditional based on settings)
def limiter_if_enabled(func):
    """Apply rate limiting only if enabled in settings"""
    if settings.ENABLE_RATE_LIMIT:
        return limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")(func)
    return func


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


@limiter_if_enabled
@router.post("/query", response_model=QueryResponse, dependencies=[auth_required])
async def query_historical_patterns(request: Request, query: QueryRequest):
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


@limiter_if_enabled
@router.get("/tickers/etf/{etf_ticker}", dependencies=[auth_required])
async def get_etf_constituents(request: Request, etf_ticker: str):
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


@limiter_if_enabled
@router.get("/prices/{ticker}", dependencies=[auth_required])
async def get_historical_prices(
    request: Request,
    ticker: str,
    start_date: str = QueryParam(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = QueryParam(None, description="End date (YYYY-MM-DD)")
):
    """
    Get historical price data for a ticker

    Returns daily price data for the specified date range.
    If no dates provided, returns last 5 years of data.
    """
    from app.services.data_service import data_service
    from datetime import datetime

    try:
        # Fetch historical data
        data = await data_service.fetch_historical_data(ticker.upper(), period="20y")

        # Convert to list of dicts for JSON response
        prices = []
        for date, row in data.iterrows():
            prices.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })

        return {
            "ticker": ticker.upper(),
            "prices": prices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {str(e)}")
