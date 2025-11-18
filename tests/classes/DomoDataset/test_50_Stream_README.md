> Last updated: 2025-11-17

# DomoStream Test Documentation

## Overview

This test suite validates the `DomoStream` class functionality including:
- Stream retrieval by ID
- Creating streams from dictionary data
- Error handling
- Backwards compatibility with legacy methods
- Configuration mapping and query extraction

## Required Environment Variables

Add these variables to your `.env` file in the project root:

```bash
# Required for all tests
DOMO_INSTANCE="your-instance-name"
DOMO_ACCESS_TOKEN="your-access-token"

# Optional - for specific stream testing
STREAM_ID_1="your-test-stream-id-1"
STREAM_ID_2="your-test-stream-id-2"
```

## How to Obtain Test Values

### Getting Your Domo Instance
Your Domo instance is the subdomain in your Domo URL:
- URL: `https://your-company.domo.com`
- Instance: `your-company`

### Getting an Access Token
1. Log into your Domo instance
2. Navigate to Admin > Authentication > Access Tokens
3. Click "Create New Token"
4. Give it a descriptive name (e.g., "Test Token")
5. Copy the generated token

### Finding Stream IDs
1. Navigate to Data Center in your Domo instance
2. Find a dataset that uses a connector (not uploaded data)
3. Click on the dataset to open details
4. The stream ID can be found in:
   - The URL: `datasources/{dataset_id}` (use the dataset's stream_id)
   - Or via API: Call `get_streams` to list available streams

Alternatively, you can run `test_cell_1` from `test_50_DomoDataset_Stream.py` to get stream IDs from your instance.

## Running the Tests

### Run all tests:
```bash
cd /home/runner/work/dl-remuxed/dl-remuxed
python tests/classes/test_50_Stream.py
```

### Run with pytest (if installed):
```bash
pytest tests/classes/test_50_Stream.py -v
```

### Run individual test functions:
```python
import asyncio
from tests.classes.test_50_Stream import test_cell_1, token_auth

# Run a specific test
asyncio.run(test_cell_1(token_auth=token_auth))
```

## Test Coverage

### test_cell_0
- **Purpose**: Verify authentication is working
- **Requirements**: DOMO_INSTANCE, DOMO_ACCESS_TOKEN
- **Expected Output**: Returns True if authenticated

### test_cell_1
- **Purpose**: Test `get_by_id()` method
- **Requirements**: STREAM_ID_1
- **Expected Output**: DomoStream instance with populated attributes

### test_cell_2
- **Purpose**: Test `from_dict()` method
- **Requirements**: None (uses sample data)
- **Expected Output**: DomoStream instance created from dictionary

### test_cell_3
- **Purpose**: Test `return_raw` parameter
- **Requirements**: STREAM_ID_1
- **Expected Output**: ResponseGetData object instead of DomoStream

### test_cell_4
- **Purpose**: Test legacy `get_stream_by_id()` method
- **Requirements**: STREAM_ID_1
- **Expected Output**: DomoStream instance (backwards compatibility)

### test_cell_5
- **Purpose**: Test error handling with invalid stream ID
- **Requirements**: None
- **Expected Output**: Stream_GET_Error exception caught

### test_cell_6
- **Purpose**: Test configuration mapping and SQL extraction
- **Requirements**: STREAM_ID_1
- **Expected Output**: Configuration report showing mapped fields

## Expected Test Results

When all tests pass, you should see:
- ✓ Authentication successful
- ✓ Stream retrieved by ID
- ✓ Stream created from dictionary
- ✓ Raw response returned correctly
- ✓ Legacy method works
- ✓ Error handling works
- ✓ Configuration extracted

## Troubleshooting

### "STREAM_ID_1 not set in .env file"
- Add STREAM_ID_1 to your .env file
- Or set it temporarily: `export STREAM_ID_1="your-stream-id"`

### "Authentication failed"
- Verify DOMO_INSTANCE is correct (no .domo.com suffix)
- Verify DOMO_ACCESS_TOKEN is valid and not expired
- Check token has appropriate permissions

### "Stream_GET_Error: Stream retrieval failed"
- Verify the stream ID exists in your instance
- Check that your token has permission to access the stream
- The stream might have been deleted

### Import Errors
- Ensure you're running from the project root
- Verify the package is installed: `pip install -e .`
- Check Python path includes the src directory

## Related Files

- **Class**: `src/domolibrary2/classes/DomoDataset/Stream.py`
- **Routes**: `src/domolibrary2/routes/stream.py`
- **Other Tests**: `tests/classes/test_50_DomoDataset_Stream.py`

## Design Patterns Validated

This test suite confirms the following design patterns are properly implemented:

1. ✓ **Entity Inheritance**: DomoStream inherits from DomoEntity
2. ✓ **Dataclass Pattern**: Uses @dataclass decorator
3. ✓ **Required Attributes**: id, auth, raw, display_url
4. ✓ **Route Delegation**: Methods call route functions
5. ✓ **Exception Handling**: Uses route-specific exceptions
6. ✓ **Standardized Signatures**: auth first, return_raw support
7. ✓ **Documentation**: All public methods have docstrings
