"""
Unified MuleSoft Service Integration

This module provides a single service class for all MuleSoft API operations
including packages, availability, and accommodation services.
"""

import logging
from typing import Dict, Any, Optional, List
import requests
from models.package_models import PackageResponseModel
from models.availability_models import AvailabilityResponse
from models.accommodation_models import Accommodation

logger = logging.getLogger(__name__)


class MuleSoftService:
    """Unified service class for all MuleSoft API integrations."""
    
    def __init__(self):
        """Initialize the MuleSoft service with common configuration."""
        self.base_url = "https://apis.orangelake.com"
        self.common_headers = {
            "X-Env": "qa",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "PostmanRuntime/7.44.1"
        }
        self.timeout = 30

    # Package-related methods
    def get_packages_mulesoft_api(self, package_id: str) -> Dict[str, Any]:
        """
        Get package details using the provided package ID.
        
        Args:
            package_id: The ID of the package to retrieve
            
        Returns:
            Dictionary containing package details (parsed with Pydantic if possible)
        """
        try:
            url = f"{self.base_url}/consumerweb/vacationPackages/orders"

            # Build parameters dict, excluding None values
            params = {}
            params["packageId"] = package_id
                
            headers = {**self.common_headers, "Accept": "*/*"}
            
            # Make the GET request to the MuleSoft API
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse the JSON response
            package_data = response.json()
            
            # Validate and parse with Pydantic model
            try:
                parsed = PackageResponseModel.model_validate(package_data)
                return parsed.model_dump()
            except Exception as e:
                logger.warning(f"Package Pydantic validation failed, returning raw data: {e}")
                return package_data
                
        except Exception as e:
            logger.error(f"Error fetching package details: {e}")
            raise

    # Availability-related methods
    def get_availabilities_mulesoft_api(self, 
                                      package_id: str,
                                      destination: str,
                                      length_of_stay: int,
                                      campaign_intitiative_id: str,
                                      accommodation_type: str,
                                      number_of_guests: int, 
                                      search_start_date: str, 
                                      search_end_date: str) -> Dict[str, Any]:
        """
        Get availability data using the provided parameters.
        
        Args:
            package_id: The ID of the package to retrieve availability for
            destination: The destination for the availability search
            length_of_stay: Length of stay in nights
            campaign_intitiative_id: Campaign initiative ID (note: intentional spelling)
            accommodation_type: Type of accommodation requested
            number_of_guests: Number of guests for the stay
            search_start_date: Start date for availability search in YYYY-MM-DD format
            search_end_date: End date for availability search in YYYY-MM-DD format
            
        Returns:
            Dictionary containing availability details (parsed with Pydantic if possible)
        """
        try:
            url = f"{self.base_url}/consumerweb/vacationPackages/orders/availabilities"
            
            # All parameters are required - set them directly
            params = {
                "packageId": package_id,
                "destination": destination,
                "lengthOfStay": length_of_stay,
                "campaignIntitiativeId": campaign_intitiative_id,
                "accommodationType": accommodation_type,
                "numberOfGuests": number_of_guests,
                "searchStartDate": search_start_date,
                "searchEndDate": search_end_date
            }
            
            logger.info(f"GET Availabilities: {url} with params {params}")
            
            # Make the GET request to the MuleSoft API
            response = requests.get(url, headers=self.common_headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse the JSON response
            availability_data = response.json()
    
            # Validate and parse with Pydantic model if possible
            try:
                parsed = AvailabilityResponse.model_validate(availability_data)
                logger.info(f"Successfully parsed availability data with Pydantic model")
                return parsed.model_dump()
            except Exception as e:
                logger.warning(f"Availability Pydantic validation failed, returning raw data: {e}")
                return availability_data
                
        except Exception as e:
            logger.error(f"Error fetching availabilities: {e}")
            raise

    # Accommodation-related methods
    def get_accommodations_mulesoft_api(self, 
                                      campaign_initiative_id: str,
                                      accommodation_type: str,
                                      length_of_stay: int,
                                      number_of_guests: int,
                                      destination: str,
                                      checkin_date: str) -> List[Dict[str, Any]]:
        """
        Get accommodation data using the provided parameters.
    
        Args:
            campaign_initiative_id: Campaign initiative ID
            accommodation_type: Type of accommodation requested
            length_of_stay: Length of stay in nights
            number_of_guests: Number of guests for the stay
            destination: The destination for the accommodation search
            checkin_date: Check-in date in YYYY-MM-DD format
    
        Returns:
            List of accommodation dictionaries (parsed with Pydantic if possible)
        """
        try:
            url = f"{self.base_url}/consumerweb/vacationPackages/orders/accommodations"
            
            # All parameters are required - set them directly
            params = {
                "campaignInitiativeId": campaign_initiative_id,
                "accommodationType": accommodation_type,
                "lengthOfStay": length_of_stay,
                "numberOfGuests": number_of_guests,
                "destination": destination,
                "checkinDate": checkin_date
            }
            
            logger.info(f"GET Accommodations: {url} with params {params}")
    
            # Make the GET request to the MuleSoft API
            response = requests.get(url, headers=self.common_headers, params=params, timeout=self.timeout)
            response.raise_for_status()
    
            # Parse the JSON response
            accommodation_data = response.json()
    
            # Try to parse each accommodation entry with the Pydantic model for validation and structure
            try:
                parsed = Accommodation.model_validate(accommodation_data)
                logger.info(f"Parsed {len(parsed)} accommodations with Pydantic model")
                return parsed.model_dump() 
            except Exception as e:
                logger.warning(f"Accommodation Pydantic validation failed, returning raw data: {e}")
                return accommodation_data
    
        except Exception as e:
            # Log any errors that occur during the API call or processing
            logger.error(f"Failed to fetch accommodations: {str(e)}")
            raise