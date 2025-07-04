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

        # Create chat agent with booking instructions
        self.agent = ChatCompletionAgent(
            kernel=self.kernel,
            name="HICVAgent",
            instructions="""
                You are an assistant for vacation package booking at Holiday Inn Club Vacations.
                You have access to package details through the PackageDetails tool.
                """,
            function_choice_behavior=FunctionChoiceBehavior.Auto()
        )
        logger.info("Created ChatCompletionAgent with Auto function choice behavior")

        # Conversation thread to preserve memory
        self.thread = ChatHistoryAgentThread()
        self._thread_created_event = asyncio.Event()
        logger.info("Initialized conversation thread")

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
            
            result = await self.kernel.invoke(plugin_name="PackageDetails", function_name="get_package_summary")
            
            package_summary = str(result)
            logger.info(f"Retrieved package summary: {package_summary[:100]}...")
            
            # Extract destination from package summary
            destination = "Unknown destination"
            for line in package_summary.split("\n"):
                if line.startswith("Destination:"):
                    destination = line.replace("Destination:", "").strip()
                    break
            
            # Format the greeting exactly as specified in the requirements
            greeting = f"Hello! I'm your vacation assistant. I'd be happy to help you plan your trip. Would you like to go ahead with this {destination} or explore some alternative options?"
            print(greeting)
            # Add the greeting to the thread
            await self.thread.on_new_message(greeting)
            logger.info(f"Added initial greeting with destination: {destination}")
            
            return greeting
        except Exception as e:
            logger.error(f"Error getting initial greeting: {str(e)}", exc_info=True)
            return "Hello! I'm your vacation assistant. I'd be happy to help you plan your trip."

    async def get_response(self, user_message: str) -> str:
        """Add user message to memory, get assistant response as string."""
        logger.info(f"Processing user message: {user_message[:50]}...")
        await self._ensure_thread_created()
        await self.thread.on_new_message(user_message)
        
        # Log that we're invoking the agent
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
