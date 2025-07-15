"""
MuleSoft Service Integration Package

This package provides integrated API services for interacting with MuleSoft APIs
for vacation booking operations. It includes three main service modules:

- package: Package-related API operations
- availability: Availability and pricing operations  
- accommodation: Accommodation search and details operations

Each module provides both class-based services for advanced usage and convenience
functions for simple operations.

Configuration is managed through the config module, which supports environment
variables for API settings.
"""

from .mulesoft_service import (MuleSoftService)