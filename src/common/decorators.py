"""
Common decorators: timing, retry, cache.
"""

from __future__ import annotations
import functools
import logging
import time
from typing import Any, Callable, Type, Tuple

logger = logging.getLogger(__name__)

# ---------------- timing ----------------
def timing(func: Callable):
    """Decorator that logs execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000  # ms
        logger.info("Function %s executed in %.2f ms", func.__name__, elapsed)
        return result
    return wrapper

# ---------------- retry -----------------
def retry(times: int = 3, exceptions: Tuple[Type[Exception], ...] = (Exception,),
          delay: float = 0.5, backoff: float = 2.0):
    """
    Retry decorator with exponential backoff.

    Parameters
    ----------
    times : attempts count
    exceptions : exceptions that trigger retry
    delay : initial delay in seconds
    backoff : multiplier applied to delay after each failure
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _delay = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times:
                        raise
                    logger.warning("Retry %s/%s after exception: %s", attempt, times, e)
                    time.sleep(_delay)
                    _delay *= backoff
        return wrapper
    return decorator

# ---------------- cache -----------------
def cache(maxsize: int = 128):
    """
    Simple LRU cache decorator.
    """
    def decorator(func: Callable):
        return functools.lru_cache(maxsize=maxsize)(func)
    return decorator
