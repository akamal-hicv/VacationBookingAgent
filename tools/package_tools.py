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

from models.package_models import PackageResponseModel

# Configure logger
logger = logging.getLogger(__name__)

class PackageDetails:
    """Tool for retrieving and displaying vacation package details."""
    
    def __init__(self):
        """Initialize the PackageDetails tool."""
        logger.info("Initializing PackageDetails tool")
        self._packages = []
        self._load_package_data()
    
    def _load_package_data(self):
        """Load package data from JSON file."""
        try:
            # Get the absolute path to the JSON file
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(current_dir, "SampleData", "PackageDetails.json")
            logger.info(f"Loading package data from {json_path}")
            
            with open(json_path, 'r') as file:
                data = json.load(file)
                logger.debug(f"Loaded JSON data: {str(data)[:200]}...")
                                
                # Convert JSON data to PackageResponseModel object
                package = PackageResponseModel(**data)
                self._packages.append(package)
                    
            logger.info(f"Successfully loaded {len(self._packages)} package(s)")
        except Exception as e:
            logger.error(f"Error loading package data: {e}", exc_info=True)
    
    @kernel_function(
        description="Get a package details",
        name="get_package_summary"
    )
    def get_package_summary(self) -> PackageResponseModel:
        """
        Get the package model object for the first available package.
        
        Returns:
            A PackageResponseModel object containing package details
        """
        logger.info("get_package_summary function called")
        if not self._packages:
            logger.warning("No packages available")
            return None
        
        logger.info(f"Returning package model: {self._packages[0].packageName}")
        return self._format_package_summary(self._packages[0])
            
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
        
        if not self._packages:
            logger.warning("No packages available to verify zip code")
            return "Unable to verify zip code: No package data available."
        
        # Normalize inputs
        confirmed_user_destination = confirmed_user_destination.strip().upper()
        user_input_zipcode = user_input_zipcode.strip()
        
        # Find the destination in the package data
        for package in self._packages:
            for dest in package.destination:
                dest_name = dest.get("destination", "")
                
                # Check if this is the confirmed destination
                if dest_name and dest_name.upper() == confirmed_user_destination:
                    logger.info(f"Found matching destination: {dest_name}")
                    
                    # Check if the zip code is in the non-qualified zip codes list
                    nq_zip_codes = dest.get("nqZipCodes", [])
                    
                    if user_input_zipcode in nq_zip_codes:
                        logger.info(f"Zip code {user_input_zipcode} is NOT valid for destination {dest_name}")
                        return f"The zip code {user_input_zipcode} is not valid for {dest_name}. Please provide a different zip code."
                    else:
                        logger.info(f"Zip code {user_input_zipcode} is valid for destination {dest_name}")
                        return f"The zip code {user_input_zipcode} is valid for {dest_name}. Let's continue with your vacation booking."
        
        logger.warning(f"No matching destination found for {confirmed_user_destination}")
        return f"Unable to verify zip code: Destination '{confirmed_user_destination}' not found in available packages."
