from fastapi import HTTPException, Request
from datetime import datetime, timedelta

async def rate_limit(request: Request, max_requests: int, interval_seconds: int):
    now = datetime.utcnow()
    last_request = request.state.last_request
    if last_request and now - last_request < timedelta(seconds=interval_seconds):
        raise HTTPException(status_code=429, detail="Too many requests")
    request.state.last_request = now
