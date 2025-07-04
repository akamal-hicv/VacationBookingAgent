"""
Pydantic models for request data structures.
"""
from enum import Enum
from pydantic import BaseModel, Field

class RequestType(str, Enum):
    """Types of requests the API can handle."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"

class ChatRequest(BaseModel):
    """Model for chat request data."""
    request_type: RequestType = Field(default=RequestType.TEXT, description="Type of request content")
    request_content: str = Field(description="The actual request content (e.g., message text)")
    request_session: str = Field(description="Unique identifier for the user's session")
