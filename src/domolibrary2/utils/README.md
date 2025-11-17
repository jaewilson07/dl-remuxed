> Last updated: 2025-10-30

# Utils Library

A comprehensive collection of utility functions for data processing, file operations, image handling, and common programming tasks. This library is designed to be standalone and reusable across different projects.

## Features

- **Async Execution Utilities**: Retry logic, concurrency control, and sequential execution
- **Data Comparison**: Deep comparison of dictionaries and lists with detailed difference reporting
- **Data Conversion**: Format conversions, datetime handling, string formatting, and validation
- **Dictionary Utilities**: Dot notation access for nested dictionaries
- **File Operations**: File and folder operations with proper error handling
- **Image Processing**: Image manipulation, base64 encoding/decoding, and comparison
- **Credential Management**: Environment file reading and credential handling
- **Password Generation**: XKCD-style password generation with customization
- **Data Upload**: Generic data upload utilities with retry logic

## Installation

### Core Dependencies

The utils library is designed to work with minimal dependencies. Core functionality only requires Python 3.8+.

```bash
# Core installation (no optional dependencies)
pip install -e .
```

### Optional Dependencies

For full functionality, install optional dependencies:

```bash
# For image processing
pip install Pillow numpy

# For pandas support
pip install pandas

# For async HTTP operations
pip install httpx

# For environment file support
pip install python-dotenv

# For date parsing
pip install python-dateutil

# For password generation
pip install xkcdpass

# For Jupyter notebook support
pip install ipython
```

### All Dependencies

```bash
pip install Pillow numpy pandas httpx python-dotenv python-dateutil xkcdpass ipython
```

## Quick Start

```python
from utils import chunk_execution, convert, DictDot, files
from utils.exceptions import UtilityError

# Async execution with retry
@chunk_execution.run_with_retry(max_retry=3)
async def my_function():
    return await some_api_call()

# Data conversion
datetime_obj = convert.convert_string_to_datetime("2023-01-01")
title_case = convert.convert_programming_text_to_title_case("get_user_data")

# Dot notation for dictionaries
data = DictDot.DictDot({"user": {"name": "John", "age": 30}})
print(data.user.name)  # "John"
print(data.user.missing)  # None (no error)

# File operations
files.upsert_file("/path/to/file.txt", "Hello, World!")
files.upsert_folder("/path/to/folder")
```

## Module Overview

### chunk_execution

Async execution utilities with retry logic and concurrency control.

```python
import asyncio
from utils import chunk_execution

# Retry decorator
@chunk_execution.run_with_retry(max_retry=3)
async def api_call():
    # Function that might fail
    return await fetch_data()

# Concurrency control
coroutines = [fetch_url(url) for url in urls]
results = await chunk_execution.gather_with_concurrency(*coroutines, n=10)

# list chunking
chunks = chunk_execution.chunk_list(large_list, chunk_size=100)
```

### compare

Data comparison utilities for dictionaries and lists.

```python
from utils import compare

dict1 = {"user": {"name": "John", "age": 30}, "items": [1, 2, 3]}
dict2 = {"user": {"name": "Jane", "age": 30}, "items": [1, 2]}

differences = compare.compare_dicts(dict1, dict2)
for diff in differences:
    print(f"{diff['key']}: {diff['message']}")
```

### convert

Data conversion utilities for various formats and types.

```python
from utils import convert
import datetime as dt

# Datetime conversions
epoch = convert.convert_datetime_to_epoch_millisecond(dt.datetime.now())
dt_obj = convert.convert_epoch_millisecond_to_datetime(epoch)

# String formatting
title = convert.convert_programming_text_to_title_case("get_user_data")
# Returns: "Get User Data"

camel = convert.convert_snake_to_pascal("user_name_field")
# Returns: "userNameField"

# Email validation
try:
    convert.test_valid_email("user@example.com")  # Returns True
except convert.InvalidEmail:
    print("Invalid email")

# DataFrame operations (requires pandas)
df_list = [df1, df2, df3]
combined_df = convert.concat_list_dataframe(df_list)
```

### DictDot

Dot notation access for dictionaries.

```python
from utils.DictDot import DictDot, split_str_to_obj

# Nested dictionary access
data = {
    "user": {
        "name": "John",
        "preferences": {"theme": "dark"}
    },
    "posts": [{"title": "Post 1"}]
}

obj = DictDot(data)
print(obj.user.name)  # "John"
print(obj.user.preferences.theme)  # "dark"
print(obj.posts[0].title)  # "Post 1"
print(obj.user.missing)  # None (no error)

# Convert pipe-separated strings
creds = split_str_to_obj(
    "instance|user@example.com|password",
    ["domo_instance", "username", "password"]
)
print(creds.domo_instance)  # "instance"
```

### files

File and folder operation utilities.

```python
from utils import files

# Create folders and files
files.upsert_folder("/path/to/folder")
files.upsert_file("/path/to/file.txt", "Hello, World!")

# Change file extensions
new_path = files.change_extension("/path/to/file.txt", ".md")

# Handle zip files
files.download_zip("/output", zip_bytes_content=zip_data)
zip_files = files.download_zip("/output", existing_zip_file_path="archive.zip")
```

### Image

Image processing and manipulation utilities (requires Pillow and numpy).

```python
from utils.Image import ImageUtils, are_same_image

# Load and process images
img = ImageUtils.from_image_file("/path/to/image.jpg")
square_img = ImageUtils.crop_square(img)
img_bytes = ImageUtils.to_bytes(img, "PNG")

# Load from bytes/base64
img = ImageUtils.from_bytestr(base64_string)

# Compare images
same = are_same_image(img1, img2)
```

### read_creds_from_dotenv

Environment credential reading utilities (requires python-dotenv).

```python
from utils import read_creds_from_dotenv

# Read all environment variables
creds = read_creds_from_dotenv.read_creds_from_dotenv(".env")
print(creds.DATABASE_URL)
print(creds.API_KEY)

# Read specific variables
creds = read_creds_from_dotenv.read_creds_from_dotenv(
    ".env",
    ["API_KEY", "SECRET_KEY"]
)
```

### xkcd_password

XKCD-style password generation utilities (requires xkcdpass).

```python
from utils import xkcd_password

# Generate basic XKCD password
password = xkcd_password.generate_xkcd_password()
print(password)  # "word1-word2-word3"

# Generate Domo-style password
password = xkcd_password.generate_domo_password()
print(password)  # "Word1-word2-word32024!"

# Custom processing
leet_password, _ = xkcd_password.process_add_leet("hello")
print(leet_password)  # "h3llo"
```

### upload_data_standalone

Generic data upload utilities with retry logic.

```python
from utils import upload_data_standalone
import asyncio

async def get_data():
    return [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]

async def upload_to_api(data):
    print(f"Uploading {len(data)} records")
    return {"success": True, "uploaded": len(data)}

# Upload with retry logic
result = await upload_data_standalone.upload_data(
    data_fn=get_data,
    upload_fn=upload_to_api,
    identifier="user_sync",
    max_retry=3
)
```

## Exception Handling

The library provides comprehensive exception handling with custom exception classes:

```python
from utils.exceptions import (
    UtilityError,          # Base exception
    InvalidEmailError,     # Email validation errors
    ConcatDataframeError,  # DataFrame operation errors
    FileOperationError,    # File operation errors
    ImageProcessingError,  # Image processing errors
    CredentialsError       # Credential reading errors
)

# Legacy exception names are also available for backwards compatibility
from utils import InvalidEmail, ConcatDataframe_InvalidElement

try:
    # Some utility operation
    pass
except UtilityError as e:
    print(f"Utility error: {e}")
    if e.details:
        print(f"Details: {e.details}")
```

## Module Availability

Check which modules are available with their dependencies:

```python
from utils import get_available_modules, get_module_info

# Check available modules
modules = get_available_modules()
print(modules)
# {
#     "chunk_execution": True,
#     "Image": True,  # True if Pillow/numpy installed
#     "upload_data": False,  # False if dependencies missing
#     ...
# }

# Get library info
info = get_module_info()
print(info)
# {
#     "name": "utils",
#     "version": "1.0.0",
#     "available_modules": {...},
#     "total_modules": 10
# }
```

## Error Handling Best Practices

```python
from utils.exceptions import UtilityError, FileOperationError

try:
    # File operations
    files.upsert_file("/protected/file.txt", "content")
except FileOperationError as e:
    print(f"File operation failed: {e}")
    print(f"Operation: {e.operation}")
    print(f"File path: {e.file_path}")

try:
    # Image processing
    img = ImageUtils.from_image_file("missing.jpg")
except ImportError:
    print("PIL not available - install with: pip install Pillow")
except FileNotFoundError:
    print("Image file not found")
except ImageProcessingError as e:
    print(f"Image processing failed: {e}")
```

## Development

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src/utils tests/
```

### Type Checking

```bash
# Install mypy
pip install mypy

# Type check
mypy src/utils/
```

## Version History

- **1.0.0**: Initial standalone release with comprehensive documentation and error handling

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues and questions:
- Check the documentation above
- Review error messages and exception details
- Check module availability with `get_available_modules()`
- Ensure required dependencies are installed
