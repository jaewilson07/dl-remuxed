# Circular Import Issue in domolibrary2

## The Problem

When you try to import `DomoDataset`, Python encounters a circular import chain that prevents the module from fully initializing.

## The Import Chain

```
1. DomoDataset/__init__.py
   ↓ imports from .core

2. DomoDataset/core.py
   ↓ imports from .dataset_default

3. DomoDataset/dataset_default.py
   ↓ imports from . import stream

4. DomoDataset/stream.py
   ↓ imports from ..DomoAccount

5. DomoAccount/__init__.py
   ↓ imports from .account_credential

6. DomoAccount/account_credential.py
   ↓ imports from ..DomoInstanceConfig.access_token

7. DomoInstanceConfig/__init__.py
   ↓ imports from . import publish

8. DomoInstanceConfig/publish.py (LINE 52-61)
   ↓ imports from .. import DomoDataset  ← CIRCULAR!
   └─ Goes back to step 1, but DomoDataset isn't finished initializing
```

## The Specific Problem Code

In `DomoInstanceConfig/publish.py` at line 52-61:

```python
class DomoPublication_Content_Enum(DomoEnumMixin, Enum):
    from .. import (
        DomoAppStudio as dmas,
        DomoCard as dmac,
        DomoDataset as dmds,  # ← This causes the circular import
        DomoPage as dmpg,
    )

    CARD = dmac.DomoCard
    DATASET = dmds.DomoDataset  # ← Tries to access DomoDataset before it's ready
    DATA_APP = dmas.DomoAppStudio
    PAGE = dmpg.DomoPage
```

**The error occurs because:**
- When Python tries to execute line 61 (`DATASET = dmds.DomoDataset`), it needs `DomoDataset` to be fully imported
- But `DomoDataset` is still in the middle of initializing (stuck at step 4, importing `stream.py`)
- Result: `AttributeError: partially initialized module 'domolibrary2.classes.DomoDataset' has no attribute 'DomoDataset'`

## Why This Happens

The enum is trying to store **class references** as enum values at **module load time**. This requires all the classes to be fully defined before the enum class body executes.

## Solutions

### Option 1: Lazy Import (Move import inside method)

Move the import from class-level to method-level so it only happens when needed:

```python
class DomoPublication_Content_Enum(DomoEnumMixin, Enum):
    CARD = "CARD"
    DATASET = "DATASET"
    DATA_APP = "DATA_APP"
    PAGE = "PAGE"

    def get_class(self):
        """Lazy-load the actual class when needed."""
        if self == self.CARD:
            from ..DomoCard import DomoCard
            return DomoCard
        elif self == self.DATASET:
            from ..DomoDataset import DomoDataset
            return DomoDataset
        elif self == self.DATA_APP:
            from ..DomoAppStudio import DomoAppStudio
            return DomoAppStudio
        elif self == self.PAGE:
            from ..DomoPage import DomoPage
            return DomoPage
```

### Option 2: Use String References (TYPE_CHECKING pattern)

Store string references instead of class objects, then resolve them later:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..DomoDataset import DomoDataset
    from ..DomoCard import DomoCard
    from ..DomoAppStudio import DomoAppStudio
    from ..DomoPage import DomoPage

class DomoPublication_Content_Enum(DomoEnumMixin, Enum):
    CARD = "domolibrary2.classes.DomoCard.DomoCard"
    DATASET = "domolibrary2.classes.DomoDataset.DomoDataset"
    DATA_APP = "domolibrary2.classes.DomoAppStudio.DomoAppStudio"
    PAGE = "domolibrary2.classes.DomoPage.DomoPage"
```

**Note:** You mentioned you don't want TYPE_CHECKING, so Option 1 is better for you.

### Option 3: Registry Pattern (Similar to your stream_config)

Use a registry that gets populated after all modules load:

```python
# In a central location
PUBLICATION_CONTENT_REGISTRY = {}

def register_publication_content(content_type: str):
    def decorator(cls):
        PUBLICATION_CONTENT_REGISTRY[content_type] = cls
        return cls
    return decorator

# Then in each class file:
@register_publication_content("DATASET")
class DomoDataset:
    pass
```

## Why Your Stream Config Works

Your stream config pattern **doesn't** have this problem because:

1. The decorator `@register_mapping` is defined **before** any imports
2. The mapping classes are imported **after** the base class and registry are defined
3. The decorator populates the registry at import time, but doesn't try to **access** the classes until you call `.search()`

```python
# stream_config.py
_MAPPING_REGISTRY = {}  # ← Registry defined first

def register_mapping(data_provider_type: str):  # ← Decorator defined
    def decorator(cls):
        _MAPPING_REGISTRY[data_provider_type] = cls
        return cls
    return decorator

@dataclass
class StreamConfig_Mapping(DomoBase):  # ← Base class defined
    pass

# NOW it's safe to import subclasses
from . import stream_configs  # ← Imports trigger @register_mapping decorators

class StreamConfig_Mappings(DomoEnumMixin, Enum):
    @classmethod
    def search(cls, value):  # ← Only ACCESS registry when method is called
        return _MAPPING_REGISTRY.get(value)()
```

The key difference: **when** the classes are accessed vs. **when** they're registered.

## Testing Without Circular Import

To test `stream_config` specifically without triggering the full import chain, you can:

```python
# Direct module import without going through DomoDataset package
import sys
sys.path.insert(0, "src")

# Import just the stream_config module file
from domolibrary2.classes.DomoDataset import stream_config

# Access the registry and functions
StreamConfig_Mapping = stream_config.StreamConfig_Mapping
_MAPPING_REGISTRY = stream_config._MAPPING_REGISTRY
```

This works because you're bypassing `DomoDataset/__init__.py` which triggers the full chain.
