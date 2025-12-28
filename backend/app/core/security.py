"""
Authentication and security utilities
"""

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
from app.core.config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> None:
    """
    Verify API key if authentication is required.

    Args:
        api_key: API key from X-API-Key header

    Raises:
        HTTPException: If authentication is required and key is invalid/missing
    """
    # If auth is not required, allow all requests
    if not settings.REQUIRE_AUTH:
        return

    # If auth is required but no keys configured, deny all
    if not settings.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication required but no API keys configured"
        )

    # Check if API key is provided and valid
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing. Please provide X-API-Key header."
        )

    if api_key not in settings.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


# Optional dependency for endpoints that should work with or without auth
async def verify_api_key_optional(api_key: Optional[str] = Security(API_KEY_HEADER)) -> Optional[str]:
    """
    Verify API key if provided, but don't require it.

    Returns the API key if valid, None otherwise.
    """
    if not settings.REQUIRE_AUTH or not api_key:
        return None

    if api_key in settings.API_KEYS:
        return api_key

    return None
