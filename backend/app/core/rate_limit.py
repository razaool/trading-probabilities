"""
Rate limiting configuration
"""

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings


def get_identifier(request: Request) -> str:
    """
    Get rate limit identifier, but skip for OPTIONS preflight requests.

    OPTIONS preflight requests should not be rate limited as they are part
    of the CORS handshake and don't represent actual API usage.
    """
    if request.method == "OPTIONS":
        return "options"  # Use a single shared bucket for all OPTIONS requests
    return get_remote_address(request)


# Create a single limiter instance
limiter = Limiter(
    key_func=get_identifier,
    default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
    storage_uri="memory://",
)
