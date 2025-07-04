"""
Pydantic models for response data structures.
"""
from enum import Enum
from pydantic import BaseModel, Field

class ResponseType(str, Enum):
    """Types of responses the API can return."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    
class ResponseCategory(str, Enum):
    """Categories of responses."""
    AGENT_RESPONSE = "agent_response"
    AGENT_INTERMEDIATE_RESPONSE = "agent_intermediate_response"

class ChatResponse(BaseModel):
    """Model for chat response data."""
    response_type: ResponseType = Field(default=ResponseType.TEXT, description="Type of response content")
    response_category: ResponseCategory = Field(default=ResponseCategory.AGENT_RESPONSE, description="Category of the response")
    response_content: str = Field(description="The actual response content")
