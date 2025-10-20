"""
Async Execution Utilities

This module provides utilities for async function execution with features like:
- Automatic retry logic with customizable error handling
- Concurrency control with semaphores
- Sequential execution of async functions
- List chunking for batch processing

Functions:
    run_with_retry: Decorator for automatic retry logic on async functions
    gather_with_concurrency: Execute multiple coroutines with concurrency limits
    run_sequence: Execute async functions sequentially
    chunk_list: Split a list into smaller chunks for batch processing

Example:
    >>> @run_with_retry(max_retry=3)
    >>> async def fetch_data():
    ...     # Function that might fail
    ...     return await api_call()

    >>> # Limit concurrent operations
    >>> results = await gather_with_concurrency(*coroutines, n=10)

    >>> # Process data in chunks
    >>> chunks = chunk_list(large_list, chunk_size=100)
"""

__all__ = ["run_with_retry", "gather_with_concurrency", "run_sequence", "chunk_list"]

import asyncio
import functools
from collections.abc import Awaitable
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union

# Import httpx with fallback for optional dependency
try:
    import httpx

    _HTTPX_AVAILABLE = True
except ImportError:
    httpx = None
    _HTTPX_AVAILABLE = False

T = TypeVar("T")


def run_with_retry(
    max_retry: int = 1, errors_to_retry_tp: Optional[Tuple[type, ...]] = None
) -> Callable:
    """
    Decorator that adds automatic retry logic to async functions.

    This decorator will retry the decorated function if it raises specified exceptions,
    with special handling for httpx.ConnectTimeout errors (if httpx is available).

    Args:
        max_retry (int): Maximum number of retry attempts (default: 1)
        errors_to_retry_tp (Tuple[type, ...], optional): Tuple of exception types
            to retry on. If None, retries on any Exception except ConnectTimeout.

    Returns:
        Callable: Decorated function with retry logic

    Example:
        >>> @run_with_retry(max_retry=3, errors_to_retry_tp=(ConnectionError,))
        >>> async def fetch_data():
        ...     return await some_api_call()

        >>> # Function will retry up to 3 times on ConnectionError
        >>> result = await fetch_data()

    Note:
        - ConnectTimeout errors (if httpx available) include a 2-second delay between retries
        - Other errors retry immediately
        - All retry attempts are logged to stdout
    """
    errors_to_retry_tp = errors_to_retry_tp or ()

    def actual_decorator(run_fn: Callable) -> Callable:
        @functools.wraps(run_fn)
        async def wrapper(*args, **kwargs):
            retry = 0
            while retry <= max_retry:
                try:
                    return await run_fn(*args, **kwargs)
                except Exception as e:
                    # Handle httpx.ConnectTimeout if httpx is available
                    if (
                        _HTTPX_AVAILABLE
                        and httpx
                        and isinstance(e, httpx.ConnectTimeout)
                    ):
                        print(f"connect timeout - retry attempt {retry} - {e}")
                        retry += 1
                        await asyncio.sleep(2)
                        if retry > max_retry:
                            raise
                        continue

                    # Only retry if error is in errors_to_retry_tp (if specified)
                    if errors_to_retry_tp and not isinstance(e, errors_to_retry_tp):
                        raise

                    print(f"retry decorator attempt - {retry} - {e}")
                    retry += 1
                    if retry > max_retry:
                        raise

        return wrapper

    return actual_decorator


async def gather_with_concurrency(
    *coros: Awaitable[T],
    n: int = 60,
) -> List[T]:
    """
    Execute multiple coroutines with concurrency control.

    Limits the number of concurrently running coroutines using a semaphore,
    preventing overwhelming of system resources or external APIs.

    Args:
        *coros: Variable number of coroutines to execute
        n (int): Maximum number of concurrent coroutines (default: 60)

    Returns:
        List[T]: Results from all coroutines in the same order as input

    Example:
        >>> async def fetch_url(url):
        ...     async with httpx.AsyncClient() as client:
        ...         return await client.get(url)

        >>> urls = ["http://example.com/1", "http://example.com/2"]
        >>> coroutines = [fetch_url(url) for url in urls]
        >>> results = await gather_with_concurrency(*coroutines, n=5)

    Note:
        This is particularly useful when making many API calls or I/O operations
        where you want to limit concurrent connections.
    """
    semaphore = asyncio.Semaphore(n)

    async def sem_coro(coro: Awaitable[T]) -> T:
        async with semaphore:
            return await coro

    return await asyncio.gather(*(sem_coro(c) for c in coros))


async def run_sequence(
    *functions: Awaitable[Any],
) -> List[Any]:
    """
    Execute a sequence of async functions sequentially.

    Executes each async function in order, waiting for each to complete
    before starting the next one. Useful when functions have dependencies
    or when you need to preserve execution order.

    Args:
        *functions: Variable number of awaitable functions to execute

    Returns:
        List[Any]: Results from all functions in execution order

    Example:
        >>> async def step1():
        ...     return "first"

        >>> async def step2():
        ...     return "second"

        >>> results = await run_sequence(step1(), step2())
        >>> print(results)  # ["first", "second"]

    Note:
        Unlike asyncio.gather(), this executes functions sequentially,
        not concurrently.
    """
    return [await function for function in functions]


def chunk_list(
    obj_ls: List[Any],
    chunk_size: int,
) -> List[List[Any]]:
    """
    Split a list into smaller chunks of specified size.

    Divides a large list into smaller sublists for batch processing.
    The last chunk may be smaller than chunk_size if the list length
    is not evenly divisible by chunk_size.

    Args:
        obj_ls (List[Any]): List of objects to split into chunks
        chunk_size (int): Maximum number of items per chunk

    Returns:
        List[List[Any]]: List of chunks, where each chunk is a list of objects

    Raises:
        ValueError: If chunk_size is less than 1

    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> chunks = chunk_list(data, chunk_size=3)
        >>> print(chunks)  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        >>> chunks = chunk_list(data, chunk_size=4)
        >>> print(chunks)  # [[1, 2, 3, 4], [5, 6, 7, 8], [9]]

    Note:
        This is useful for processing large datasets in smaller batches
        to manage memory usage or API rate limits.
    """
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")

    if not obj_ls:
        return []

    return [
        obj_ls[i * chunk_size : (i + 1) * chunk_size]
        for i in range((len(obj_ls) + chunk_size - 1) // chunk_size)
    ]
