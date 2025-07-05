"""
Pydantic models for availability-related data structures.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Tour(BaseModel):
    """Model for tour information."""
    tourId: int = Field(description="Tour identifier")
    numberAvailable: int = Field(description="Number of available slots")
    time: str = Field(description="Tour time")


class TourDate(BaseModel):
    """Model for tour date information."""
    tourDate: str = Field(description="Date in YYYY-MM-DD format")
    tours: List[Tour] = Field(description="List of available tours on this date")


class AvailableDateRange(BaseModel):
    """Model for available date range with tour information."""
    firstNight: str = Field(description="First night of stay in YYYY-MM-DD format")
    lastNight: str = Field(description="Last night of stay in YYYY-MM-DD format")
    tourDates: List[TourDate] = Field(description="List of available tour dates within this range")


class AvailabilityResponse(BaseModel):
    """Model for availability response."""
    destination: str = Field(description="Destination location")
    campaign: str = Field(description="Campaign identifier")
    availableDates: List[AvailableDateRange] = Field(description="List of available date ranges with nested tour information")


class AvailabilityRequest(BaseModel):
    """Model for availability request."""
    numberOfGuests: int = Field(description="Number of guests for the stay")
    searchStartDate: str = Field(description="Start date for availability search in YYYY-MM-DD format")
    searchEndDate: str = Field(description="End date for availability search in YYYY-MM-DD format")


class Availability_Model(BaseModel):
    """Container model for availability request and response."""
    request: AvailabilityRequest = Field(description="Availability request parameters")
    response: Optional[AvailabilityResponse] = Field(None, description="Availability response data")
