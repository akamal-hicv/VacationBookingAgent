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
        description="Get a summary of the package details",
        name="get_package_summary"
    )
    def get_package_summary(self) -> str:
        """
        Get a summary of all available package details.
        
        Returns:
            A string containing summaries of all available packages
        """
        logger.info("get_package_summary function called")
        if not self._packages:
            logger.warning("No packages available to summarize")
            return "No packages available."
            
        logger.info(f"Returning summary for package: {self._packages[0].packageName}")
        return self._format_package_summary(self._packages[0])
            
    def _format_package_summary(self, package: PackageResponseModel) -> str:
        """Format a package summary string."""
        logger.debug(f"Formatting summary for package ID: {package.packageId}")
        summary = f"Package Summary: {package.packageName} (ID: {package.packageId})\n\n"
        
        # Extract destination name from the destination list
        destination_name = "Unknown destination"
        if package.destination and len(package.destination) > 0:
            destination_name = package.destination[0].get("destination", "Unknown destination")
            
        summary += f"Destination: {destination_name}\n"
        summary += f"Accommodation: {package.accommodationType}\n"
        summary += f"Package Expiration: {package.packageExpiration}\n"

        return summary
