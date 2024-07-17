#!/usr/bin/env python3
"""
A module for using the Redis NoSQL data storage.

This module provides a Cache class to interact with Redis, enabling storage,
retrieval, and tracking of data.
"""

import uuid
import redis
from functools import wraps
from typing import Any, Callable, Union, Optional


def count_calls(method: Callable) -> Callable:
    """
    Tracks the number of calls made to a method in the Cache class.

    Args:
        method (Callable): The method to track.

    Returns:
        Callable: The wrapped method with call counting.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Invokes the given method after incrementing its call counter."""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Tracks the call details of a method in the Cache class.

    Args:
        method (Callable): The method to track.

    Returns:
        Callable: The wrapped method with input/output tracking.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Returns the method's output after storing its inputs and output."""
        in_key = f'{method.__qualname__}:inputs'
        out_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    Displays the call history of a Cache class' method.

    Args:
        fn (Callable): The method to replay the history of.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = f'{fxn_name}:inputs'
    out_key = f'{fxn_name}:outputs'
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print(f'{fxn_name} was called {fxn_call_count} times:')
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print(f'{fxn_name}(*{fxn_input.decode("utf-8")}) -> {fxn_output}')


class Cache:
    """
    Represents an object for storing data in a Redis data storage.

    This class provides methods to store, retrieve data,track method calls.
    """
    def __init__(self) -> None:
        """Initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The key under which the data is stored.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from a Redis data storage.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optio[Callable], opt): The def to apply to the retrieved data

        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            str: The retrieved string data.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            int: The retrieved integer data.
        """
        return self.get(key, lambda x: int(x))
