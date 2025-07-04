"""
Pydantic models for package-related data structures.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PackageResponseModel(BaseModel):
    """Model for vacation package details."""
    # Required fields
    campaignId: str = Field(description="Campaign identifier")
    packageId: str = Field(description="Unique identifier for the package")
    packageExpiration: str = Field(description="Package expiration date")
    accommodationType: str = Field(description="Type of accommodation")
    packageName: str = Field(description="Name of the package")
    
    # Fields with different structure in JSON
    destination: List[Dict[str, Any]] = Field(default=[], description="Destination information")
    