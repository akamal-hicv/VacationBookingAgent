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
    destination: List[Dict[str, Any]] = Field(default=[], description="Primary destination information")
    alternateDestinations: List[Dict[str, Any]] = Field(default=[], description="Alternative destinations information")
    
    @property
    def length_of_stay(self) -> int:
        """
        Extract the length of stay from the package name.
        Example: "3 Night Resort" -> 3
        
        Returns:
            int: The length of stay in nights, or 0 if not found
        """
        import re
        if not self.packageName:
            return 0
            
        # Extract the first number from the package name
        match = re.search(r'\d+', self.packageName)
        if match:
            return int(match.group())
        return 0
    