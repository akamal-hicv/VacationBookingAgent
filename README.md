# AI Package Sales Agent

A chat-based sales agent for vacation packages using Semantic Kernel and FastAPI.

## Project Structure

```
.
├── agent_garden/       # Agent lifecycle management
├── agents/            # Agent implementations
├── controllers/       # FastAPI controllers
├── models/            # Pydantic data models
├── static/            # Frontend assets
├── system/            # System configuration
├── tools/             # Agent tools
└── SampleData/        # Sample data for testing
```

## Features

- Session-based agent caching with TTL
- Structured request/response models using Pydantic
- Clean separation of concerns with modular architecture
- Web-based chat UI

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python main.py`

## API Structure

- **Request Models**:
  - `RequestType` enum: TEXT, IMAGE, AUDIO
  - `ChatRequest` with fields for request type, content, and session

- **Response Models**:
  - `ResponseType` enum: TEXT, IMAGE, AUDIO
  - `ResponseCategory` enum: AGENT_RESPONSE, AGENT_INTERMEDIATE_RESPONSE
  - `ChatResponse` with fields for response type, category, and content
