# ignore_folders Parameter - Usage Guide

## Overview
The `ignore_folders` parameter allows you to exclude specific folders/paths when retrieving or downloading Jupyter workspace content.

## How It Works
- **Matches path segments**: Filters based on folder names in the path hierarchy
- **Example**: `ignore_folders=['domolibrary']` will exclude any path containing 'domolibrary' as a segment
  - ✓ Filters: `domolibrary/test.py`
  - ✓ Filters: `scripts/domolibrary/config.py`
  - ✗ Doesn't filter: `my_domolibrary_script.py` (substring, not segment)

## Usage Examples

### Route Level (Low-level API)

```python
from domolibrary2.routes.jupyter import content as jupyter_routes
import domolibrary2.auth as dmda

auth = dmda.DomoJupyterAuth(
    domo_instance="your-instance",
    jupyter_token="your-token",
)

# Get content excluding specific folders
res = await jupyter_routes.get_content(
    auth=auth,
    ignore_folders=['domolibrary', 'temp', '.git'],
    return_raw=True,
)

print(f"Retrieved {len(res.response)} items (excluding ignored folders)")
```

### Class Level (High-level API)

```python
import domolibrary2.classes.DomoJupyter as dmj

ws = dmj.DomoJupyterWorkspace(...)

# Get content excluding folders
content = await ws.get_content(
    ignore_folders=['domolibrary', '.ipynb_checkpoints', 'recent_executions']
)

# Download workspace excluding folders
await ws.download_workspace_content(
    base_export_folder='../../EXPORTS/jupyter/',
    replace_folder=True,
    ignore_folders=['domolibrary', 'temp', 'node_modules'],
)
```

## Common Use Cases

### 1. Exclude Library Folders
```python
ignore_folders=['domolibrary', 'node_modules', 'venv', '.venv']
```

### 2. Exclude Generated/Temp Files
```python
ignore_folders=[
    '.ipynb_checkpoints',
    'recent_executions',
    'temp',
    '__pycache__',
]
```

### 3. Exclude Version Control
```python
ignore_folders=['.git', '.github', '.vscode']
```

### 4. Combined Strategy
```python
ignore_folders=[
    # Libraries
    'domolibrary', 'node_modules', 'venv',
    # Generated files
    '.ipynb_checkpoints', 'recent_executions', '__pycache__',
    # Version control
    '.git', '.github',
]
```

## Testing

Example test path filtering:
```python
test_path = "recent_executions/3._account_deploy.ipynb/2025-07-17/stdout"

# This WILL be filtered (recent_executions is a path segment)
ignore_folders = ['recent_executions']
# Result: Path is excluded ✓

# This will NOT be filtered (domolibrary is not in this path)
ignore_folders = ['domolibrary']
# Result: Path is included ✗
```

## Implementation Details

### Path Segment Matching
```python
# Filters based on path segments
f["path"].split("/")  # ['recent_executions', 'file.ipynb', 'stdout']
'recent_executions' in segments  # True - will be filtered
```

### Recursive Application
The `ignore_folders` parameter is passed through all recursive calls, ensuring consistent filtering at every level of the directory tree.

## API Signature

### Route Function
```python
async def get_content(
    auth: DomoJupyterAuth,
    content_path: str = "",
    ignore_folders: list[str] = None,  # ← New parameter
    is_recursive: bool = True,
    is_skip_recent_executions: bool = True,
    is_skip_default_files: bool = True,
    session: httpx.AsyncClient | None = None,
    debug_api: bool = False,
    debug_num_stacks_to_drop: int = 2,
    parent_class: Optional[str] = None,
    return_raw: bool = False,
) -> ResponseGetData
```

### Class Methods
```python
async def get_content(
    self,
    debug_api: bool = False,
    return_raw: bool = False,
    is_recursive: bool = True,
    content_path: str = "",
    ignore_folders: list[str] = None,  # ← New parameter
    session: httpx.AsyncClient | None = None,
)

async def download_workspace_content(
    self,
    base_export_folder=None,
    replace_folder: bool = True,
    ignore_folders: list[str] = None,  # ← New parameter
    debug_api: bool = False,
    session: httpx.AsyncClient | None = None,
) -> str
```

## Migration Notes

### Backward Compatibility
- ✓ Fully backward compatible - `ignore_folders` defaults to `None`
- ✓ Existing code continues to work without changes
- ✓ No breaking changes to existing API

### Upgrade Path
Simply add the `ignore_folders` parameter to existing calls:
```python
# Before
await ws.download_workspace_content(replace_folder=True)

# After
await ws.download_workspace_content(
    replace_folder=True,
    ignore_folders=['domolibrary', 'temp']
)
```
