"""
Tools for handling vacation package details.
"""
import json
import os
import logging
from typing import List, Optional
import logging
 
import semantic_kernel as sk
from semantic_kernel.functions import kernel_function, KernelFunction
from semantic_kernel.functions.kernel_arguments import KernelArguments
from datasource.mulesoft_service import MuleSoftService
 
from system.config import PACKAGE_ID
from models.package_models import PackageResponseModel
 
# Configure logger
logger = logging.getLogger(__name__)
 
class PackageDetails:
    """Tool for retrieving and displaying vacation package details."""
   
    def __init__(self):
        """Initialize the PackageDetails tool."""
        logger.info("Initializing PackageDetails tool")
        self._package = None
        self._load_package_data()
   
    def _load_package_data(self):
        """Load package data from MuleSoft API."""
        try:

           
            mulesoft_service = MuleSoftService()
            api_response = mulesoft_service.get_packages_mulesoft_api(PACKAGE_ID)
            self._package = PackageResponseModel(**api_response)
 
            logger.info(f"Successfully loaded package from MuleSoft API: {self._package.packageName}")
 
        except Exception as e:
            logger.error(f"Error loading package data: {e}", exc_info=True)
   
    @kernel_function(
        description="Get package details",
        name="get_package_summary"
    )
    def get_package_summary(self) -> PackageResponseModel:
        """
        Get the package model object.
       
        Returns:
            A PackageResponseModel object containing package details
        """
        logger.info("get_package_summary function called")
        if not self._package:
            logger.warning("No package available")
            return None
       
        logger.info(f"Returning package model: {self._package.packageName}")
        return self._format_package_summary(self._package)
           
    def _format_package_summary(self, package: PackageResponseModel) -> PackageResponseModel:
        """Return the package model directly."""
        logger.debug(f"Returning package model for ID: {package.packageId}")
        return package
       
    @kernel_function(
        description="Verify if a zip code is valid for a confirmed destination",
        name="ZipCodeVerification"
    )
    def ZipCodeVerification(self, confirmed_user_destination: str, user_input_zipcode: str) -> str:
        """
        Verify if a user-provided zip code is valid for a confirmed destination.
       
        Args:
            confirmed_user_destination: The destination name that the user has confirmed
            user_input_zipcode: The zip code provided by the user
           
        Returns:
            A string indicating whether the zip code is valid for the destination
        """
        logger.info(f"Verifying zip code {user_input_zipcode} for destination {confirmed_user_destination}")
       
        if not self._package:
            logger.warning("No package available to verify zip code")
            return "Unable to verify zip code: No package data available."
       
        # Normalize inputs
        confirmed_user_destination = confirmed_user_destination.strip().upper()
        user_input_zipcode = user_input_zipcode.strip()
       
        # Check primary destinations first
        for dest in self._package.destination:
            dest_name = dest.get("destination", "")
           
            # Check if this is the confirmed destination
            if dest_name and dest_name.upper() == confirmed_user_destination:
                logger.info(f"Found matching primary destination: {dest_name}")
               
                # Check if the zip code is in the non-qualified zip codes list
                nq_zip_codes = dest.get("nqZipCodes", [])
               
                if user_input_zipcode in nq_zip_codes:
                    logger.info(f"Zip code {user_input_zipcode} is NOT valid for primary destination {dest_name}")
                    return f"The zip code {user_input_zipcode} is not valid for {dest_name}. Please select a different destination."
                else:
                    logger.info(f"Zip code {user_input_zipcode} is valid for primary destination {dest_name}")
                    return f"The zip code {user_input_zipcode} is valid for {dest_name}. Let's continue with your vacation booking."
       
        # If not found in primary destinations, check alternative destinations
        for alt_dest in self._package.alternateDestinations:
            alt_dest_name = alt_dest.get("destination", "")
           
            # Check if this is the confirmed destination
            if alt_dest_name and alt_dest_name.upper() == confirmed_user_destination:
                logger.info(f"Found matching alternative destination: {alt_dest_name}")
               
                # Check if the zip code is in the non-qualified zip codes list
                nq_zip_codes = alt_dest.get("nqZipCodes", [])
               
                if user_input_zipcode in nq_zip_codes:
                    logger.info(f"Zip code {user_input_zipcode} is NOT valid for alternative destination {alt_dest_name}")
                    return f"The zip code {user_input_zipcode} is not valid for {alt_dest_name}. Please select a different destination."
                else:
                    logger.info(f"Zip code {user_input_zipcode} is valid for alternative destination {alt_dest_name}")
                    return f"The zip code {user_input_zipcode} is valid for {alt_dest_name}. Let's continue with your vacation booking."
       
        logger.warning(f"No matching destination found for {confirmed_user_destination} in primary or alternative destinations")
        return f"Unable to verify zip code: Destination '{confirmed_user_destination}' not found in available package destinations."
 
 