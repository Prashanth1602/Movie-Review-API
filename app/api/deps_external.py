from fastapi import Header, HTTPException, status, Depends
from app.core.config import settings
from app.core.rate_limiter import RateLimiter
import os
from dotenv import load_dotenv

load_dotenv()

limiter = RateLimiter(rate=5.0, capacity=10.0)

def verify_api_key(x_api_key: str = Header(...)):
    expected_key = os.getenv("EXTERNAL_API_KEY")
    
    if not expected_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: EXTERNAL_API_KEY not set"
        )

    if x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    if not limiter.check_rate_limit(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    return x_api_key
