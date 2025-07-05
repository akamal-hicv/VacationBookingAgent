"""
Tools for handling availability-related functionality.
"""
import json
import os
import logging
from typing import List, Optional

from semantic_kernel.functions.kernel_function_decorator import kernel_function
from models.availability_models import (
    Availability_Model, 
    AvailabilityRequest, 
    AvailabilityResponse,
    AvailableDateRange,
    TourDate,
    Tour
)

# Configure logging
logger = logging.getLogger(__name__)


class AvailabilityDetails:
    """Class for handling availability-related operations."""
    
    def __init__(self):
        """Initialize the AvailabilityDetails class."""
        self._availabilities = None
        self.load_availabilities()
    
    def load_availabilities(self) -> None:
        """
        Load availability data from the JSON file.
        """
        try:
            # Get the absolute path to the JSON file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_file_path = os.path.join(current_dir, "SampleData", "availabilities.json")
            
            logger.info(f"Loading availabilities from {json_file_path}")
            
            with open(json_file_path, "r") as file:
                self._availabilities = json.load(file)
                logger.info("Availabilities loaded successfully")
        except Exception as e:
            logger.error(f"Error loading availabilities: {str(e)}")
            self._availabilities = None
    
    @kernel_function(
        description="Get availability information for a date range",
        name="get_availability"
    )
    def get_availability(self, number_of_guests: int, search_start_date: str, search_end_date: str) -> AvailabilityResponse:
        """
        Get availability information for a specified date range and number of guests.
        
        Args:
            number_of_guests: Number of guests for the stay
            search_start_date: Start date for availability search in YYYY-MM-DD format
            search_end_date: End date for availability search in YYYY-MM-DD format
            
        Returns:
            An AvailabilityResponse object containing availability details
        """
        logger.info(f"get_availability function called with guests: {number_of_guests}, start: {search_start_date}, end: {search_end_date}")
        
        if not self._availabilities:
            logger.warning("No availabilities data loaded")
            return None
        
        # Filter available dates that fall within the search range
        filtered_data = self._availabilities.copy()
        filtered_data["availableDates"] = [
            date_range for date_range in self._availabilities.get("availableDates", [])
            if (date_range["firstNight"] >= search_start_date and 
                date_range["lastNight"] <= search_end_date)
        ]
        
        # Convert filtered JSON data to Pydantic models using our helper method
        response = self._format_availability_summary(filtered_data)
        
        logger.info(f"Returning availability response with {len(response.availableDates)} date ranges")
        return response
    
    @kernel_function(
        description="Get availability summary with tour dates and times",
        name="get_availability_summary"
    )
    def get_availability_summary(self) -> AvailabilityResponse:
        """
        Get the availability summary with first/last night date ranges and tour dates/times.
        
        Returns:
            An AvailabilityResponse object containing availability details
        """
        logger.info("get_availability_summary function called")
        
        if not self._availabilities:
            logger.warning("No availabilities data loaded")
            return None
        
        # Convert the JSON data to Pydantic models
        response = self._format_availability_summary(self._availabilities)
        
        logger.info(f"Returning availability summary with {len(response.availableDates)} date ranges")
        return response
        
    def _format_availability_summary(self, availability_data) -> AvailabilityResponse:
        """
        Format the availability data into a proper Pydantic model structure.
        
        Args:
            availability_data: Raw availability data from JSON
            
        Returns:
            An AvailabilityResponse object with properly structured nested models
        """
        # Convert available dates
        available_dates = []
        for date_range in availability_data.get("availableDates", []):
            # Convert tour dates
            tour_dates = []
            for tour_date_entry in date_range.get("tourDates", []):
                # Convert tours
                tours = []
                for tour_entry in tour_date_entry.get("tours", []):
                    tour = Tour(
                        tourId=tour_entry.get("tourId"),
                        numberAvailable=tour_entry.get("numberAvailable"),
                        time=tour_entry.get("time")
                    )
                    tours.append(tour)
                
                tour_date = TourDate(
                    tourDate=tour_date_entry.get("tourDate"),
                    tours=tours
                )
                tour_dates.append(tour_date)
            
            available_date_range = AvailableDateRange(
                firstNight=date_range.get("firstNight"),
                lastNight=date_range.get("lastNight"),
                tourDates=tour_dates
            )
            available_dates.append(available_date_range)
        
        # Create the response
        response = AvailabilityResponse(
            destination=availability_data.get("destination", ""),
            campaign=availability_data.get("campaign", ""),
            availableDates=available_dates
        )
        
        return response
