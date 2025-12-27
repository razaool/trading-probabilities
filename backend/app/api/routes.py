"""
API route definitions
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, TickerListResponse
from app.services.query_service import query_service
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
        top_stocks=[],  # To be populated later
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
