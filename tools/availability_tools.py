"""
Tools for handling availability-related functionality.
"""
import json
import os
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from datasource.mulesoft_service import MuleSoftService
from system.config import PACKAGE_ID

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
    def __init__(self):
        self._availabilities = {}

    @kernel_function(
        description="Get availability information for a date range. Package details should be obtained from a previous PackageDetails-get_package_summary call.",
        name="get_availability"
    )
    def get_availability(
        self, 
        number_of_guests: int, 
        search_start_date: str, 
        search_end_date: str,
        destination: str,
        length_of_stay: int,
        campaign_initiative_id: str,
        accommodation_type: str
    ) -> AvailabilityResponse:
        """
        Load availability data dynamically from MuleSoft API using package details and user inputs.
        All package information must be provided as arguments from a previous PackageDetails call.
        
        Args:
            number_of_guests: Number of guests for the stay
            search_start_date: Start date for availability search in YYYY-MM-DD format
            search_end_date: End date for availability search in YYYY-MM-DD format
            destination: Destination that the user confirms
            package_id: Package ID(packageId field) available in the PackageDetails
            length_of_stay: Length of stay(lengthOfStay field) available in the PackageDetails 
            campaign_initiative_id: Initiative(initiative field) available in the PackageDetails
            accommodation_type: Accommodation type(accommodationType field) available in the PackageDetails
            
        Returns:
            AvailabilityResponse object with availability data
        """
        logger.info(f"load_availabilities called with guests: {number_of_guests}, start: {search_start_date}, end: {search_end_date}, destination: {destination}")
        
        try:
            package_id = PACKAGE_ID 
        
            logger.info(f"Using package data - ID: {package_id}, Destination: {destination}, "
                    f"Length: {length_of_stay}, Campaign: {campaign_initiative_id}, Type: {accommodation_type}")
            
            # Load availability data from MuleSoft API

            mulesoft_service = MuleSoftService()
            api_response = mulesoft_service.get_availabilities_mulesoft_api(
                destination=destination.upper(),
                package_id=package_id,
                length_of_stay=length_of_stay,
                campaign_intitiative_id=campaign_initiative_id,
                accommodation_type=accommodation_type.lower(),
                number_of_guests=number_of_guests,
                search_start_date=search_start_date,
                search_end_date=search_end_date
            )

            self._availabilities = api_response

            # Filter available dates that overlap with the search range
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
    
        except Exception as e:
            error_msg = f"Failed to load availability data: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self._availabilities = None
            return None
        
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
                lastNight=(datetime.strptime(date_range.get("lastNight"), "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d"),
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
