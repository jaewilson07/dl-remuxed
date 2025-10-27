# DomoPage Access Module - Test Configuration

## Overview
This document describes the environment variables required for testing the DomoPage access module functionality.

## Required Environment Variables

### Core Authentication
These variables are required for all tests:

```bash
DOMO_INSTANCE="your-instance-name"
DOMO_ACCESS_TOKEN="your-access-token"
```

**How to obtain:**
1. Navigate to your Domo instance
2. Go to Admin > Authentication > Access Tokens
3. Create a new access token or use an existing one
4. Note: The authenticated user must have appropriate permissions for the pages being tested

### Test Page IDs
These variables are used to test page access functionality:

```bash
TEST_PAGE_ID_1="123456789"    # Required: A page the authenticated user has access to
TEST_PAGE_ID_2="987654321"    # Optional: A page the authenticated user does NOT have access to (for exception testing)
```

**How to obtain:**
1. Navigate to a page in your Domo instance
2. The page ID is in the URL: `https://your-instance.domo.com/page/PAGE_ID`
3. For `TEST_PAGE_ID_1`: Choose any page you own or have access to
4. For `TEST_PAGE_ID_2`: Choose a page you don't have access to (or leave empty to skip exception tests)

### Optional: Group ID for Sharing Tests
This variable enables group sharing tests:

```bash
TEST_GROUP_ID="123"    # Optional: A group ID for testing group sharing functionality
```

**How to obtain:**
1. Navigate to Admin > Governance Toolkit > Groups
2. Select a group
3. The group ID is in the URL: `https://your-instance.domo.com/groups/GROUP_ID`
4. Note: Tests will share pages with this group, so use a test group

## Complete .env File Example

```bash
# Domo Authentication
DOMO_INSTANCE="mycompany"
DOMO_ACCESS_TOKEN="your-token-here"

# Page Access Tests
TEST_PAGE_ID_1="384424178"           # A page you have access to
TEST_PAGE_ID_2="790951325"           # Optional: A page you don't have access to

# Optional Group Sharing Tests
TEST_GROUP_ID="456"                  # Optional: Test group for sharing tests
```

## Running Tests

### Run all tests:
```bash
cd /home/runner/work/dl-remuxed/dl-remuxed
python tests/classes/test_50_DomoPage_Access.py
```

### Run with pytest (if available):
```bash
pytest tests/classes/test_50_DomoPage_Access.py -v
```

### Run specific tests:
```bash
pytest tests/classes/test_50_DomoPage_Access.py::test_cell_3_get_accesslist -v
```

## Test Coverage

The test suite covers:

1. **test_page_access()** method:
   - Basic access testing
   - Return raw response option
   - Exception handling

2. **get_accesslist()** method:
   - Retrieve comprehensive access list
   - User and group enumeration
   - Ownership information enrichment
   - Return raw response option

3. **share()** method:
   - Share with single user
   - Share with multiple users
   - Share with groups
   - Error handling

## Notes

- All tests are designed to be safe and non-destructive
- Sharing tests only share with the authenticated user (safe operation)
- Tests gracefully skip if required environment variables are not configured
- Exception tests verify proper error handling without requiring actual access failures

## Troubleshooting

**"Skipping test - TEST_PAGE_ID_1 not configured"**
- Set the `TEST_PAGE_ID_1` environment variable in your `.env` file

**"Page not found" errors**
- Verify the page ID exists and is accessible
- Check that the authenticated user has access to the page

**"Authentication failed" errors**
- Verify `DOMO_ACCESS_TOKEN` is valid and not expired
- Ensure the token has appropriate permissions

**Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.9 or higher
