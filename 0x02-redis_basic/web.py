#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.

This module provides a get_page function to obtain HTML content
from a URL, cache the result, and track access counts.
"""

import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""The module-level Redis instance."""


def count_and_cache(method: Callable) -> Callable:
    """
    Decorator to cache the output of fetched data and count URL accesses.

    Args:
        method (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapped function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        The wrapper function for caching the output and counting accesses.
        """
        count_key = f'count:{url}'
        cache_key = f'cached:{url}'

        redis_store.incr(count_key)
        
        cached_result = redis_store.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')

        result = method(url)
        redis_store.setex(cache_key, 10, result)
        return result

    return wrapper


@count_and_cache
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the req, res and track the req

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))

