"""
Tools for handling accommodation-related functionality.
"""
import json
import os
import logging
from typing import List, Optional
from datetime import datetime, timedelta

from semantic_kernel.functions.kernel_function_decorator import kernel_function
from models.accommodation_models import (
    AccommodationResponse,
    Accommodation
)

# Configure logging
logger = logging.getLogger(__name__)


class AccommodationDetails:
    """Class for handling accommodation-related operations."""
    
    def __init__(self):
        """Initialize the AccommodationDetails class."""
        self._accommodations = None
        self.load_accommodations()
    
    def load_accommodations(self) -> None:
        """
        Load accommodation data from the JSON file.
        """
        try:
            # Get the absolute path to the JSON file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_file_path = os.path.join(current_dir, "SampleData", "accommodations.json")
            
            logger.info(f"Loading accommodations from {json_file_path}")
            
            with open(json_file_path, "r") as file:
                self._accommodations = json.load(file)
                logger.info(f"Accommodations loaded successfully: {len(self._accommodations)} properties found")
        except Exception as e:
            logger.error(f"Error loading accommodations: {str(e)}")
            self._accommodations = None
    
    @kernel_function(
        description="Get accommodation details for a specific check-in date and length of stay",
        name="get_accommodation_details"
    )
    def get_accommodation_details(self, checkin_date: str, length_of_stay: int) -> AccommodationResponse:
        """
        Get accommodation details for a specified check-in date and length of stay.
        
        Args:
            checkin_date: Check-in date in YYYY-MM-DD format
            length_of_stay: Length of stay in nights
            
        Returns:
            An AccommodationResponse object containing available accommodation options
        """
        logger.info(f"get_accommodation_details called with: checkin_date={checkin_date}, length={length_of_stay}")
        
        if not self._accommodations:
            logger.warning("No accommodations data loaded")
            return AccommodationResponse(accommodations=[])
        
        # Filter accommodations based on check-in date and length of stay
        filtered_accommodations = []
        
        for accommodation in self._accommodations:
            # Check if the accommodation's first night matches the requested check-in date
            if accommodation["firstNight"] == checkin_date:
                # Calculate the expected last night based on length of stay
                checkin_dt = datetime.strptime(checkin_date, "%Y-%m-%d")
                expected_last_night = (checkin_dt + timedelta(days=length_of_stay - 1)).strftime("%Y-%m-%d")
                
                # Check if the accommodation's last night is greater than or equal to the expected last night
                if accommodation["lastNight"] >= expected_last_night:
                    filtered_accommodations.append(accommodation)
        
        # Map 'name' field to 'AccommodationName' to match the model requirements
        for acc in filtered_accommodations:
            if 'name' in acc and 'AccommodationName' not in acc:
                acc['AccommodationName'] = acc['name']
                
        response = AccommodationResponse(accommodations=[Accommodation.parse_obj(acc) for acc in filtered_accommodations])
        
        logger.info(f"Returning accommodation response with {len(response.accommodations)} options")
        return response
