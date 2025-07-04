import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import logging

from models.request_models import ChatRequest
from models.response_models import ChatResponse

from agents.vacation_agent import VacationChatAgent
from agent_garden.agent_cache import agent_cache

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Vacation Chatbot")

# Register cache cleanup task with FastAPI lifecycle
agent_cache.start_cleanup_task(app)

# Mount static directory (for JS / CSS if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the chat UI from static folder."""
    return FileResponse("static/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_req: ChatRequest):
    """Handle chat message using session-specific agent instances."""
    # Get or create agent for this session
    is_new_session = not await agent_cache.exists(chat_req.request_session)
    agent = await agent_cache.get(chat_req.request_session)
    
    # For new sessions, always get initial greeting that includes package destination
    if is_new_session:
        # Log that we're handling a new session
        logger.info(f"New session detected: {chat_req.request_session}")
        print("New session detected: ", chat_req.request_session)
        # Always send initial greeting for new sessions
        logger.info("New session, sending initial greeting")
        response_text = await agent.get_initial_greeting()
        logger.info(f"Initial greeting generated: {response_text[:50]}...")
        
        # If there's actual content in the request, process it in the next request
        if chat_req.request_content and chat_req.request_content.strip():
            logger.info(f"User provided initial message: {chat_req.request_content[:50]}... - Will be processed in next request")
    else:
        # Get response using the session's agent for existing sessions
        logger.info(f"Existing session: {chat_req.request_session}")
        response_text = await agent.get_response(chat_req.request_content)
    
    # Create a structured response
    response = ChatResponse(
        response_type=chat_req.request_type.value,  # Match response type to request type
        response_category="agent_response",
        response_content=str(response_text)  # Ensure response is converted to string
    )
    
    return response
