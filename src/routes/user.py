"""
User Management Routes - Compatibility Layer

This module provides backward compatibility imports from the new user module structure.
All user-related functionality has been reorganized into:
- user/user.py: Core user operations
- user/attributes.py: User attribute management  
- user/properties.py: User property management

This file maintains the original import interface for backward compatibility.
"""

# Import everything from the new user module structure
from .user import *
