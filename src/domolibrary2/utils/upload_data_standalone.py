"""
Generic Data Upload Utilities

This module provides generic utilities for uploading data with retry logic,
error handling, and logging. This is a standalone version that doesn't
depend on the Domo library, making it reusable for other projects.

Functions:
    loop_upload: Generic upload function with retry logic
    upload_data: Main data upload orchestration function

Example:
    >>> import asyncio
    >>> import pandas as pd
    >>>
    >>> async def my_upload_function(data, **kwargs):
    ...     # Your custom upload logic here
    ...     print(f"Uploading {len(data)} rows")
    ...     return {"success": True}
    >>>
    >>> async def my_data_function():
    ...     return pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    >>>
    >>> # Upload data with retry logic
    >>> result = await upload_data(
    ...     data_fn=my_data_function,
    ...     upload_fn=my_upload_function,
    ...     identifier="test_upload"
    ... )

Note:
    This is a generic version of upload_data.py that can be adapted for
    various data upload scenarios. For Domo-specific functionality,
    see the original upload_data.py file.
"""

__all__ = ["loop_upload", "upload_data"]

from typing import Any, Callable, Dict, Optional

# Optional dependencies
try:
    import pandas as pd

    _PANDAS_AVAILABLE = True
except ImportError:
    pd = None
    _PANDAS_AVAILABLE = False

try:
    import httpx

    _HTTPX_AVAILABLE = True
except ImportError:
    httpx = None
    _HTTPX_AVAILABLE = False


class SimpleLogger:
    """
    Simple logger implementation for cases where no external logger is provided.
    """

    def __init__(self, app_name: str = "upload_data"):
        self.app_name = app_name

    def log_info(self, message: str):
        print(f"[INFO] {self.app_name}: {message}")

    def log_warning(self, message: str):
        print(f"[WARNING] {self.app_name}: {message}")

    def log_error(self, message: str):
        print(f"[ERROR] {self.app_name}: {message}")


async def loop_upload(
    upload_data: Any,
    upload_fn: Callable,
    identifier: str,
    logger: Optional[Any] = None,
    debug_fn: bool = True,
    max_retry: int = 2,
    **upload_kwargs,
) -> Dict[str, Any]:
    """
    Upload data with automatic retry logic.

    Args:
        upload_data (Any): Data to upload
        upload_fn (Callable): Function to perform the upload
        identifier (str): Identifier for this upload (for logging)
        logger (Any, optional): Logger instance with log_info, log_warning, log_error methods
        debug_fn (bool): Enable debug printing
        max_retry (int): Maximum number of retry attempts
        **upload_kwargs: Additional arguments passed to upload_fn

    Returns:
        Dict[str, Any]: Upload result from upload_fn

    Raises:
        Exception: If all retry attempts fail

    Example:
        >>> async def my_upload(data, target="api"):
        ...     if len(data) > 0:
        ...         return {"success": True, "rows": len(data)}
        ...     return {"success": False}
        >>>
        >>> result = await loop_upload(
        ...     upload_data=[1, 2, 3],
        ...     upload_fn=my_upload,
        ...     identifier="test_upload",
        ...     target="my_api"
        ... )
    """
    if logger is None:
        logger = SimpleLogger()

    data_size = len(upload_data) if hasattr(upload_data, "__len__") else "unknown"
    base_msg = f"{identifier}"

    if debug_fn:
        print(
            f"Starting upload of {data_size} items for {base_msg} with {max_retry} attempts"
        )

    retry_attempt = 1
    result = None

    while retry_attempt <= max_retry and not result:
        try:
            if debug_fn:
                print(f"Attempt {retry_attempt}/{max_retry} for {base_msg}")

            result = await upload_fn(upload_data, **upload_kwargs)

        except Exception as e:
            retry_attempt += 1

            message = f"⚠️ Upload error: {e} in {identifier} during retry attempt {retry_attempt}/{max_retry}"
            logger.log_warning(message)
            if debug_fn:
                print(message)

    if not result:
        raise Exception(
            f"💣 Failed to upload {data_size} items for {base_msg} - {retry_attempt}/{max_retry} retries reached"
        )

    return result


async def upload_data(
    data_fn: Callable,
    upload_fn: Callable,
    identifier: str = "upload",
    session: Optional[Any] = None,
    debug_fn: bool = True,
    debug_api: bool = False,
    logger: Optional[Any] = None,
    max_retry: int = 2,
    **kwargs,
) -> Optional[Dict[str, Any]]:
    """
    Main data upload orchestration function.

    Executes a data function to get data, then uploads it using the provided
    upload function with automatic retry logic and comprehensive logging.

    Args:
        data_fn (Callable): Function that returns data to upload
        upload_fn (Callable): Function that performs the actual upload
        identifier (str): Identifier for this upload operation
        session (Any, optional): HTTP session or connection object
        debug_fn (bool): Enable debug function printing
        debug_api (bool): Enable API debug mode
        logger (Any, optional): Logger instance
        max_retry (int): Maximum retry attempts
        **kwargs: Additional arguments passed to data_fn and upload_fn

    Returns:
        Optional[Dict[str, Any]]: Upload result, or None if no data to upload

    Example:
        >>> async def get_user_data():
        ...     return [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
        >>>
        >>> async def upload_to_api(data):
        ...     print(f"Uploading {len(data)} users")
        ...     return {"success": True, "uploaded": len(data)}
        >>>
        >>> result = await upload_data(
        ...     data_fn=get_user_data,
        ...     upload_fn=upload_to_api,
        ...     identifier="user_sync"
        ... )
    """
    if logger is None:
        logger = SimpleLogger("upload_data")

    try:
        message = f"🏁 Starting data upload: {identifier} - {data_fn.__name__}"
        logger.log_info(message)
        if debug_fn:
            print(message)

        # Create session if needed and httpx is available
        local_session = None
        if session is None and _HTTPX_AVAILABLE:
            local_session = httpx.AsyncClient()
            session = local_session

        # Execute data function
        if session:
            upload_data_result = await data_fn(
                session=session, debug_api=debug_api, **kwargs
            )
        else:
            upload_data_result = await data_fn(debug_api=debug_api, **kwargs)

        # Check if we have data to upload
        if upload_data_result is None:
            message = f"No data returned from {data_fn.__name__} for {identifier}"
            logger.log_info(message)
            if debug_fn:
                print(message)
            return None

        # Check for empty pandas DataFrame
        if _PANDAS_AVAILABLE and pd and isinstance(upload_data_result, pd.DataFrame):
            if len(upload_data_result.index) == 0:
                message = (
                    f"Empty DataFrame returned from {data_fn.__name__} for {identifier}"
                )
                logger.log_info(message)
                if debug_fn:
                    print(message)
                return None

        # Check for empty list/collection
        if hasattr(upload_data_result, "__len__") and len(upload_data_result) == 0:
            message = f"Empty data collection returned from {data_fn.__name__} for {identifier}"
            logger.log_info(message)
            if debug_fn:
                print(message)
            return None

        if debug_fn:
            data_preview = (
                upload_data_result[:5]
                if hasattr(upload_data_result, "__getitem__")
                else str(upload_data_result)[:100]
            )
            print(f"Data preview: {data_preview}")

        # Perform upload with retry logic
        result = await loop_upload(
            upload_data=upload_data_result,
            upload_fn=upload_fn,
            identifier=identifier,
            debug_fn=debug_fn,
            max_retry=max_retry,
            logger=logger,
            session=session,
            debug_api=debug_api,
            **kwargs,
        )

        # Log results
        success = (
            result.get("success", True) if isinstance(result, dict) else bool(result)
        )
        if success:
            message = f"🚀 Successful upload: {identifier} in {data_fn.__name__}"
            logger.log_info(message)
        else:
            message = (
                f"💣 Upload completed but reported failure: {identifier} - {result}"
            )
            logger.log_error(message)

        if debug_fn:
            print(message)

        return result

    except Exception as e:
        message = f"💀 Critical error in upload_data for {identifier}: {e}"
        logger.log_error(message)
        if debug_fn:
            print(message)
        raise

    finally:
        # Clean up local session if created
        if local_session:
            await local_session.aclose()
