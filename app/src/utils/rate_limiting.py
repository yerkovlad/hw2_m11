from fastapi import HTTPException, Request
from datetime import datetime, timedelta

async def rate_limit(request: Request, max_requests: int, interval_seconds: int):
    """
    Limits the number of requests that can be made in a given time interval.

    :param request: The incoming HTTP request.
    :param max_requests: Maximum number of allowed requests in the interval.
    :param interval_seconds: The time interval in seconds.
    :raises HTTPException: If the rate limit is exceeded.
    """
    now = datetime.utcnow()
    last_request = request.state.last_request
    if last_request and now - last_request < timedelta(seconds=interval_seconds):
        raise HTTPException(status_code=429, detail="Too many requests")
    request.state.last_request = now
