"""
Tools for handling accommodation-related functionality.
"""
import json
import os
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from datasource.mulesoft_service import MuleSoftService

from semantic_kernel.functions.kernel_function_decorator import kernel_function
from models.accommodation_models import (
    AccommodationResponse,
    Accommodation
)

# Configure logging
logger = logging.getLogger(__name__)

class AccommodationDetails:
    def __init__(self):
        self._accommodations = None

    @kernel_function(
        description="Get accommodation details for a specific check-in date and length of stay",
        name="get_accommodation_details"
    )
    def get_accommodation_details(self, checkin_date: str, length_of_stay: int, destination: str, number_of_guests: int, campaign_initiative_id: str,accommodation_type: str) -> AccommodationResponse:
        """
        Get accommodation details for a specified check-in date and length of stay.
        Loads data from MuleSoft API and filters based on criteria.
        
        Args:
            checkin_date: Check-in date in YYYY-MM-DD format
            length_of_stay: Length of stay(lengthOfStay field) available in the PackageDetails 
            destination: Destination confirmed by the user
            number_of_guests: Number of guests for the stay
            campaign_initiative_id: Initiative(initiative field) available in the PackageDetails
            accommodation_type: Accommodation type(accommodationType field) available in the PackageDetails
            
        Returns:
            An AccommodationResponse object containing available accommodation options
        """
        logger.info(f"get_accommodation_details called with: checkin_date={checkin_date}, length={length_of_stay}, destination={destination}, guests={number_of_guests}")
        
        try:
            mulesoft_service = MuleSoftService()
            
            api_response = mulesoft_service.get_accommodations_mulesoft_api(                
                length_of_stay=length_of_stay,          
                campaign_initiative_id=campaign_initiative_id,  
                accommodation_type=accommodation_type.lower(),
                number_of_guests=number_of_guests,
                destination=destination.upper(),
                checkin_date=checkin_date
            )

            self._accommodations = api_response
            
            logger.info(f"Successfully loaded accommodation data for {destination}")

            # Filter accommodations based on check-in date and length of stay
            filtered_accommodations = []
            
            if self._accommodations:
                for accommodation in self._accommodations:
                    # Check if the accommodation's first night matches the requested check-in date
                    if accommodation.get("firstNight") == checkin_date:
                        # Calculate the expected last night based on length of stay
                        checkin_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
                        expected_last_night = (checkin_dt + timedelta(days=length_of_stay - 1)).strftime("%Y-%m-%d")
                        
                        # Check if the accommodation's last night is greater than or equal to the expected last night
                        if accommodation.get("lastNight", "") >= expected_last_night:
                            filtered_accommodations.append(accommodation)
            
            # Map 'name' field to 'AccommodationName' to match the model requirements
            for acc in filtered_accommodations:
                if 'name' in acc and 'AccommodationName' not in acc:
                    acc['AccommodationName'] = acc['name']
                    
            response = AccommodationResponse(accommodations=[Accommodation.parse_obj(acc) for acc in filtered_accommodations])
            
            logger.info(f"Returning accommodation response with {len(response.accommodations)} options")
            return response

        except Exception as e:
            error_msg = f"Failed to load accommodation data: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self._accommodations = None
            return AccommodationResponse(accommodations=[])