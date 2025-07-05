"""
Pydantic models for accommodation-related data structures.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class RoomType(BaseModel):
    """Model for room type information."""
    propertyRoomTypeId: int = Field(description="Property room type identifier")
    roomTypeCode: str = Field(description="Room type code")
    description: str = Field(description="Room type description")
    occupancy: int = Field(description="Maximum occupancy")


class Accommodation(BaseModel):
    """Model for accommodation information."""
    firstNight: str = Field(description="First night of stay in YYYY-MM-DD format")
    lastNight: str = Field(description="Last night of stay in YYYY-MM-DD format")
    propertyCode: str = Field(description="Property code identifier")
    AccommodationName: str = Field(description="Property name/ Accommodation Name")
    roomTypes: List[RoomType] = Field(description="List of available room types")


class AccommodationResponse(BaseModel):
    """Model for accommodation response."""
    accommodations: List[Accommodation] = Field(description="List of available accommodations")


class AccommodationRequest(BaseModel):
    """Model for accommodation request."""
    checkinDate: str = Field(description="Check-in date in YYYY-MM-DD format")
    destination: str = Field(description="Confirmed destination")
    numberOfGuests: int = Field(description="Number of guests for the stay")
    lengthOfStay: int = Field(description="Length of stay in nights")


class Accommodation_Model(BaseModel):
    """Container model for accommodation request and response."""
    request: AccommodationRequest = Field(description="Accommodation request parameters")
    response: Optional[AccommodationResponse] = Field(None, description="Accommodation response data")
