import asyncio
import logging
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.agents.chat_completion.chat_completion_agent import ChatHistoryAgentThread
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

import logging
logger = logging.getLogger(__name__)

from system.config import (
    DEPLOYMENT_NAME,
    AZURE_ENDPOINT,
    AZURE_API_KEY,
    AZURE_API_VERSION,
)

# Use relative import with sys.path modification
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.package_tools import PackageDetails
from tools.availability_tools import AvailabilityDetails
from tools.accommodation_tools import AccommodationDetails

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("vacation_agent")

class VacationChatAgent:
    """Encapsulates Azure-based Semantic-Kernel chat agent with thread memory."""

    def __init__(self) -> None:
        logger.info("Initializing VacationChatAgent")
        # Initialize kernel and OpenAI service
        self.kernel = Kernel()
        service = AzureChatCompletion(
            deployment_name=DEPLOYMENT_NAME,
            endpoint=AZURE_ENDPOINT,
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
        )
        self.kernel.add_service(service)
        logger.info(f"Added Azure Chat Completion service: {DEPLOYMENT_NAME}")
        
        # Register the PackageDetails tool with the kernel
        package_details = PackageDetails()
        self.kernel.add_plugin(package_details, "PackageDetails")
        logger.info("Registered PackageDetails plugin with kernel")
        
        # Register the AvailabilityDetails tool with the kernel
        availability_details = AvailabilityDetails()
        self.kernel.add_plugin(availability_details, "AvailabilityDetails")
        logger.info("Registered AvailabilityDetails plugin with kernel")
        
        # Register the AccommodationDetails tool with the kernel
        accommodation_details = AccommodationDetails()
        self.kernel.add_plugin(accommodation_details, "AccommodationDetails")
        logger.info("Registered AccommodationDetails plugin with kernel")

        # Create chat agent with booking instructions
        self.agent = ChatCompletionAgent(
            kernel=self.kernel,
            name="HICVAgent",
            instructions="""
                You are an assistant for vacation package booking at Holiday Inn Club Vacations.
                You have access to package details through the PackageDetails tool, availability information through the AvailabilityDetails tool, and accommodation options through the AccommodationDetails tool.
                Guide the user to flowing conversation:
                1. You need to help the user to confirm the destination.(The inital message has the destination and package details)
                2. If the user is not ready to go with the primary destination then suggest the alternative destinations. Always suggest the top 5 alternative destinations and ask do you have any specific alternative destination if so check the alternative destination is available in the package or not.
                3. If the user confirms the destination, ask to provide the zip code of current location. 
                4. If the user provides the zip code, verify the zip code using the ZipCodeVerification tool in PackageDetails plugin.
                5. After zip code verification, ask the user for the number of guests .
                6. Next the goal is to collect the guest's preferred date range for their stay in a natural, conversational manner, as if speaking in a live call. Guide the user step-by-step:
                6 a. Ask if the guest already has specific dates in mind for their stay.
                6 b. If not, suggest considering this month as an option.
                6 c. If they decline, ask them to pick a month they are interested in.
                6 d. Once a month is selected, ask if they have a specific week in that month in mind.
                6 e. Use the guest's response to construct a dateStartRange.
                6 f. IMPORTANT: Use the length of stay from the package details (LengthOfTheStay) to calculate the corresponding dateEndRange. DO NOT ask the user how many nights they want to stay.
                6 g. Finally, call the AvailabilityDetails tool using the generated dateStartRange and dateEndRange.
                7. Use the AvailabilityDetails tool to check availability for the specified dates (which would be always future date i.e. greater than today's date) and number of guests.
                8. When presenting available date options to the user:
                    a. Present ONLY date ranges in a clearly numbered list (e.g., "1. October 1-3, 2025", "2. October 2-4, 2025")
                    b. Ask the user to select a specific option 
                    c. Wait for the user to select one specific date range before proceeding
                    d. Do NOT mention or list any tour dates at this stage
                9. After the user selects a specific date range option:
                    a. Confirm their selected date range
                    b. Only then present the available tour dates for THAT SPECIFIC date range without showing any tour times
                    c. Ask the user to select a preferred tour date from the available options
                    d. Example: "You've selected October 1-3, 2025. Available tour dates are: 1. October 2, 2025 2. October 3, 2025. Please select your preferred tour date."
                10. After the user confirms the tour date:
                    a. Confirm their selected tour date
                    b. Only then present the available tour times for THAT SPECIFIC tour date
                    c. Ask the user to select a preferred tour time from the available options
                    d. Example: "You've selected October 2, 2025 for your tour. Available times are: 1. 8:30 AM 2. 11:00 AM 3. 1:00 PM 4. 6:00 PM. Please select your preferred tour time."
                11. After confirming the tour details, use the AccommodationDetails tool to get accommodation options based on the confirmed check-in date and length of stay from the package.
                12. When presenting accommodation options to the user:
                    a. First, ONLY present the available accommodation property names in a numbered list
                    b. Do NOT show room types at this stage
                    c. Ask the user to select a specific accommodation property by number
                    d. Example: "Here are the available accommodations: 1. Holiday Inn Club Vacations at Orange Lake Resort 2. Holiday Inn Club Vacations Cape Canaveral Beach Resort. Please select your preferred accommodation."
                13. After the user selects a specific accommodation property:
                    a. Confirm their selected accommodation property
                    b. Only then present the available room types for THAT SPECIFIC accommodation
                    c. Present room types in a numbered list
                    d. Ask the user to select a preferred room type
                    e. Example: "You've selected Holiday Inn Club Vacations at Orange Lake Resort. Here are the available room types: 1. Resort - 1 Bedroom (Occupancy: 4) 2. Resort - 2 Bedroom (Occupancy: 8). Please select your preferred room type."
                14. After the user selects a room type, confirm their selection.
                15. Only after ALL selections are complete (date range, tour date, tour time, accommodation property Name, and room type), provide a complete summary of their booking details.

                Guardrail: 
                1. Only respond based on the values explicitly provided in the tool input. Do not generate or infer any information beyond the given context.
                While responding look the below points
                1. Always act friendly and professional, and guide the user clearly through the booking process. Be intelligent about understanding ask question if you didn't understand properly.
                2. Always don't generate multiple question in a simple response try to ask one by one.  
                3. Make sure each question is asked as a separate prompt, with a conversational, helpful tone that feels natural in audio interaction.           
                """,
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )
        logger.info("Created ChatCompletionAgent with Auto function choice behavior")

        # Conversation thread to preserve memory
        self.thread = ChatHistoryAgentThread()
        self._thread_created_event = asyncio.Event()
        logger.info("Initialized conversation thread")
        
        # Add UserContext state to maintain confirmed variables
        self.user_context = {
            "confirmed_destination": None,
            "zip_code_verified": False,
            "user_zip_code": None,
            "number_of_guests": None,
            "search_start_date": None,
            "search_end_date": None,
            "confirmed_checkin_date": None,
            "length_of_stay": None,
            "selected_accommodation_type": None,
            "selected_property_code": None,
            "selected_room_type": None,
        }

    async def _ensure_thread_created(self):
        if not self._thread_created_event.is_set():
            logger.info("Creating new conversation thread")
            await self.thread.create()
            self._thread_created_event.set()

    async def get_initial_greeting(self) -> str:
        """Get an initial greeting message that includes package destination info."""
        logger.info("Getting initial greeting message")
        await self._ensure_thread_created()
        
        try:
            # Use the PackageDetails tool through the kernel
            logger.info("Attempting to get package details")
            
            function_result = await self.kernel.invoke(plugin_name="PackageDetails", function_name="get_package_summary")
        
            # Extract the actual PackageResponseModel from the FunctionResult
            package_model = function_result.value
        
            # Log the package details
            logger.info(f"Retrieved package model: {package_model.packageId}")
        
            # Extract primary destination from package model
            destination = "Unknown destination"
            if package_model.destination and len(package_model.destination) > 0:
                destination = package_model.destination[0].get("destination", "Unknown destination")
            
            # Extract alternative destinations
            alternative_destinations = []
            if hasattr(package_model, 'alternateDestinations') and package_model.alternateDestinations:
                for alt_dest in package_model.alternateDestinations:
                    if alt_dest.get("isActive", False) and alt_dest.get("isMarketable", False):
                        alternative_destinations.append(alt_dest.get("destination", ""))
            
            # Store destinations in user_context for later use
            self.user_context["package_destination"] = destination
            self.user_context["alternative_destinations"] = alternative_destinations
            
            logger.info(f"Primary destination: {destination}")
            logger.info(f"Alternative destinations: {alternative_destinations}")
            
            greeting = f"Hello! I'm your vacation assistant. I'd be happy to help you plan your trip. Would you like to go ahead with this {destination}?"
            print(greeting)
            # Add the greeting to the thread
            await self.thread.on_new_message(greeting)
            logger.info(f"Added initial greeting with destination: {destination}")
            print("Added initial greeting with destination: {destination}")                     
            
            return greeting
        except Exception as e:
            logger.error(f"Error getting initial greeting: {str(e)}", exc_info=True)
            return "Hello! I'm your vacation assistant. I'd be happy to help you plan your trip."

    async def get_response(self, user_message: str) -> str:
        """Add user message to memory, get assistant response as string."""
        logger.info(f"Processing user message: {user_message[:50]}...")
        print(user_message)
        await self._ensure_thread_created()
        await self.thread.on_new_message(user_message)
                
        # Log that we're invoking the agent for normal responses
        logger.info("Invoking agent to get response")
        try:
            response = await self.agent.get_response(thread=self.thread)
            
            # Enhanced logging for function calls
            if hasattr(response, 'function_calls') and response.function_calls:
                logger.info(f"Agent made {len(response.function_calls)} function call(s)")
                for i, func_call in enumerate(response.function_calls):
                    logger.info(f"Function call #{i+1}: {func_call.name}")
                    logger.info(f"  Arguments: {func_call.arguments}")
                    if hasattr(func_call, 'result') and func_call.result:
                        # Log the result but truncate if it's too long
                        result_str = str(func_call.result)
                        if len(result_str) > 500:
                            result_str = result_str[:500] + "... [truncated]"
                        logger.info(f"  Result: {result_str}")
            else:
                logger.info("No function calls were made in this response")
            
            return response.content
        except Exception as e:
            logger.error(f"Error getting agent response: {str(e)}", exc_info=True)
            return f"Sorry, I encountered an error: {str(e)}"
