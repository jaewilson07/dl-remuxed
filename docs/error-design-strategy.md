# Domo Library Error Design Strategy

## Overview

This document outlines the comprehensive error strategy for the Domo Library, providing a structured approach to exception handling that improves debugging, user experience, and API development.

## Core Error Hierarchy

### Base Exception Classes

```python
DomoError                    # Base for all Domo-related errors
├── RouteError              # API route/endpoint errors  
├── ClassError              # Class instance errors (DomoDataset, DomoCard, etc.)
└── AuthError               # Authentication-specific errors
```

## Route Error Categories

For most API routes, implement these four core error types:

### 1. GET Errors - `{Module}_GET_Error`
**Purpose**: Failed retrieval operations
**When to Use**: 
- API returns 4xx/5xx status codes during GET requests
- Data parsing failures
- Malformed responses

**Naming Convention**: `{ModuleName}_GET_Error`

**Examples**:
```python
class Dataset_GET_Error(RouteError): pass
class User_GET_Error(RouteError): pass
class Card_GET_Error(RouteError): pass
```

### 2. Search Not Found - `Search{Module}_NotFound`
**Purpose**: Specific searches that return no results
**When to Use**:
- Search operations return empty results when results were expected
- Entity lookups fail to find matching records
- Distinguishes between "no permission" vs "doesn't exist"

**Naming Convention**: `Search{ModuleName}_NotFound` or `{ModuleName}_SearchNotFound`

**Examples**:
```python
class SearchDataset_NotFound(RouteError): pass
class SearchUser_NotFound(RouteError): pass
class SearchRole_NotFound(RouteError): pass
```

### 3. CRUD Errors - `{Module}_CRUD_Error`
**Purpose**: Create, Update, Delete operation failures
**When to Use**:
- POST/PUT/DELETE operations fail
- Data validation errors during mutations
- Permission denied for modifications

**Naming Convention**: `{ModuleName}_CRUD_Error`

**Examples**:
```python
class Dataset_CRUD_Error(RouteError): pass
class User_CRUD_Error(RouteError): pass
class Card_CRUD_Error(RouteError): pass
```

### 4. Sharing Errors - `{Module}Sharing_Error`
**Purpose**: Permission and sharing-related failures
**When to Use**:
- Share/unshare operations fail
- Permission grant/revoke failures
- Access control violations

**Naming Convention**: `{ModuleName}Sharing_Error`

**Examples**:
```python
class DatasetSharing_Error(RouteError): pass
class CardSharing_Error(RouteError): pass
class PageSharing_Error(RouteError): pass
```

## Authentication Error Strategy

Authentication requires a more granular approach due to various failure modes:

### Base Auth Error
```python
class AuthError(RouteError):
    """Base for all authentication-related errors"""
```

### Specific Auth Errors
```python
class InvalidCredentialsError(AuthError):
    """Username/password, tokens, or API keys are invalid"""
    
class InvalidInstanceError(AuthError):
    """Domo instance URL is invalid or inaccessible"""
    
class AccountLockedError(AuthError):
    """User account is locked due to failed attempts or policy"""
    
class InvalidAuthTypeError(AuthError):
    """Wrong authentication method for the API endpoint"""
    
class TokenExpiredError(AuthError):
    """Access token or session has expired"""
    
class InsufficientPermissionsError(AuthError):
    """Valid auth but lacks required permissions"""
    
class MFARequiredError(AuthError):
    """Multi-factor authentication step required"""
    
class NoAccessTokenReturned(AuthError):
    """Auth API didn't return expected token"""

class RateLimitExceededError(AuthError):
    """Authentication rate limit exceeded"""
```

## Specialized Error Categories

### Data Operation Errors
```python
class DataUploadError(RouteError):
    """Specific to data upload failures"""
    
class DataExportError(RouteError):
    """Specific to data export failures"""
    
class SchemaValidationError(RouteError):
    """Data schema doesn't match expectations"""
```

### Configuration Errors
```python
class ConfigurationError(RouteError):
    """Instance configuration issues"""
    
class FeatureNotAvailableError(RouteError):
    """Requested feature not available in instance"""
```

## Error Usage Guidelines

### When to Create New Error Types

**CREATE** a new error type when:
- The error represents a distinct failure mode requiring different handling
- Users need to catch and handle this specific error differently
- The error provides additional context not covered by base classes

**DON'T CREATE** a new error type when:
- The error is just a different message for the same underlying issue
- It's a one-off error that won't be reused
- The base RouteError or existing category is sufficient

### Error Message Best Practices

1. **Be Specific**: Include entity IDs, operation details
2. **Be Actionable**: Suggest what the user should do
3. **Include Context**: Show what was attempted
4. **Preserve Original**: Include API response when helpful

**Good Examples**:
```python
# Specific and actionable
"Failed to retrieve dataset 'abc123'. Verify dataset exists and you have read permission."

# Includes context
"Unable to create user with email 'user@example.com'. Email already exists in instance."

# Preserves API context
"Dataset upload failed during stage 2. API returned: 'Schema validation error - column 'date' expected DATE format'"
```

### Error Construction Patterns

#### Standard Route Error
```python
class Dataset_GET_Error(RouteError):
    def __init__(self, dataset_id: str = None, response_data=None, **kwargs):
        super().__init__(
            entity_id=dataset_id,
            response_data=response_data,
            **kwargs
        )
```

#### Search Not Found with Context
```python
class SearchDataset_NotFound(RouteError):
    def __init__(self, search_query: str, response_data=None, **kwargs):
        message = f"No datasets found matching search criteria: '{search_query}'"
        super().__init__(
            message=message,
            response_data=response_data,
            additional_context={"search_query": search_query},
            **kwargs
        )
```

#### Auth Error with Specific Context
```python
class InvalidAuthTypeError(AuthError):
    def __init__(self, required_auth_types: List[str], current_auth_type: str = None, **kwargs):
        auth_list = ", ".join(required_auth_types)
        message = f"This API requires one of: {auth_list}"
        if current_auth_type:
            message += f" (provided: {current_auth_type})"
            
        super().__init__(
            message=message,
            additional_context={
                "required_auth_types": required_auth_types,
                "current_auth_type": current_auth_type
            },
            **kwargs
        )
```

## Error Handling Patterns

### Try-Catch Patterns

```python
# Specific error handling
try:
    dataset = await get_dataset(dataset_id)
except SearchDataset_NotFound:
    # Handle missing dataset specifically
    dataset = await create_default_dataset()
except Dataset_GET_Error as e:
    # Handle other retrieval issues
    logger.error(f"Dataset retrieval failed: {e}")
    raise

# Auth error handling
try:
    auth = await get_full_auth(instance, username, password)
except InvalidCredentialsError:
    # Prompt for correct credentials
    raise LoginRequiredError("Please check your username and password")
except AccountLockedError:
    # Redirect to account unlock
    raise AccountIssueError("Account is locked. Contact administrator")
except AuthError as e:
    # Handle any other auth issues
    logger.error(f"Authentication failed: {e}")
    raise
```

### Error Recovery Patterns

```python
# Retry with different auth type
try:
    result = await api_call(full_auth)
except InvalidAuthTypeError as e:
    if "DeveloperAuth" in e.additional_context.get("required_auth_types", []):
        result = await api_call(developer_auth)
    else:
        raise

# Fallback search strategies
try:
    users = await search_users_by_email(email)
except SearchUser_NotFound:
    # Try partial match
    users = await search_users_by_partial_email(email)
```

## Implementation Checklist

For each new route module, implement:

- [ ] `{Module}_GET_Error` - for retrieval failures
- [ ] `Search{Module}_NotFound` - for empty search results  
- [ ] `{Module}_CRUD_Error` - for create/update/delete failures
- [ ] `{Module}Sharing_Error` - for permission/sharing issues (if applicable)
- [ ] Specific errors for unique failure modes
- [ ] Comprehensive docstrings with examples
- [ ] Unit tests for error scenarios
- [ ] Error recovery examples in documentation

## Migration Strategy

1. **Phase 1**: Standardize existing error classes to follow naming conventions
2. **Phase 2**: Add missing error categories to existing routes
3. **Phase 3**: Update error handling in client classes
4. **Phase 4**: Add comprehensive error recovery examples
5. **Phase 5**: Create error monitoring and analytics

## AI Assistant Guidelines

When working with this library, follow these patterns:

1. **Always** use specific error types rather than generic exceptions
2. **Include** entity IDs and relevant context in error messages  
3. **Preserve** original API responses for debugging
4. **Suggest** recovery actions when possible
5. **Test** error scenarios as thoroughly as success paths
6. **Document** expected errors for each function

## Benefits

This error strategy provides:

- **Consistent**: Predictable error types across all modules
- **Debuggable**: Rich context for troubleshooting
- **Recoverable**: Specific errors enable targeted recovery
- **Maintainable**: Clear patterns for adding new error types
- **User-Friendly**: Actionable error messages
- **Monitorable**: Structured errors enable better observability

## Examples in Practice

### Dataset Route Errors
```python
# /src/routes/dataset.py
class Dataset_GET_Error(RouteError): pass
class SearchDataset_NotFound(RouteError): pass  
class Dataset_CRUD_Error(RouteError): pass
class DatasetSharing_Error(RouteError): pass
class DataUploadError(RouteError): pass           # Specialized
class SchemaValidationError(RouteError): pass    # Specialized
```

### User Route Errors  
```python
# /src/routes/user.py
class User_GET_Error(RouteError): pass
class SearchUser_NotFound(RouteError): pass
class User_CRUD_Error(RouteError): pass  
class UserSharing_Error(RouteError): pass
class CreateUser_MissingRole(RouteError): pass   # Specialized
class UserAvatar_Error(RouteError): pass         # Specialized
```

### Application Route Errors
```python
# /src/routes/application.py  
class Application_GET_Error(RouteError): pass
class SearchApplication_NotFound(RouteError): pass
class Application_CRUD_Error(RouteError): pass
class ApplicationSharing_Error(RouteError): pass
class AppDeployment_Error(RouteError): pass      # Specialized
class AppManifest_Error(RouteError): pass        # Specialized
```

This strategy ensures consistent, debuggable, and maintainable error handling across the entire Domo Library.