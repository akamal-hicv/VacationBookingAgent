
# AI Vacation Package Sales Agent

A conversational AI agent for helping the user for completing the vacation packages using Microsoft's Semantic Kernel, Azure OpenAI, and FastAPI. This agent guides potential customers through the vacation booking process with a natural, step-by-step conversation flow.

## Project Overview

This project implements an AI-powered vacation sales agent that helps users book vacation packages by:

1. Collecting user preferences (destination, dates, number of guests)
2. Presenting available date ranges and tour options
3. Guiding users through accommodation selection
4. Providing a complete booking summary

The agent uses a sequential, conversational approach to avoid overwhelming users with too many options at once.

## Project Structure

```
.
├── agent_cache/         # Session-based agent caching with TTL
│   └── agent_cache.py   # Agent cache logic
├── agents/              # Agent implementations with conversation logic
│   └── vacation_agent.py
├── controllers/         # FastAPI controllers for web endpoints
│   └── controller.py
├── datasource/          # Data integration and sample data
│   ├── mulesoft_service.py
│   └── SampleData/
│       ├── accommodations.json
│       ├── availabilities.json
│       └── PackageDetails.json
├── models/              # Pydantic data models for validation
│   ├── accommodation_models.py
│   ├── availability_models.py
│   ├── package_models.py
│   ├── request_models.py
│   └── response_models.py
├── static/              # Frontend assets and chat UI
│   └── index.html
├── system/              # System configuration and environment settings
│   └── config.py
├── tools/               # Specialized agent tools
│   ├── accommodation_tools.py
│   ├── availability_tools.py
│   └── package_tools.py
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── README.md
```

## Technical Implementation

- **Semantic Kernel**: Foundation for building AI agents with tool-calling capabilities
- **Azure OpenAI Integration**: Powers the conversational AI
- **FastAPI**: Handles HTTP requests and serves the web interface
- **Pydantic Models**: Ensures data validation and type safety
- **Session Management**: Agent cache for per-session conversations

## Specialized Tools

- **PackageDetails**: Retrieves and validates vacation package information
- **AvailabilityDetails**: Manages tour date and time availability
- **AccommodationDetails**: Handles accommodation and room type selection

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure OpenAI API access

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/vacation-booking-agent.git
   cd vacation-booking-agent
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On Unix/MacOS
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   - Create a `.env` file with your Azure OpenAI credentials:
     ```
     AZURE_DEPLOYMENT_NAME=your-deployment-name
     AZURE_ENDPOINT=your-azure-endpoint
     AZURE_API_KEY=your-api-key
     AZURE_API_VERSION=2024-12-01-preview
     PACKAGE_ID=your-package-id
     ```

5. Run the application
   ```bash
   python main.py
   ```

6. Access the chat interface at [http://localhost:8081](http://localhost:8081)

## Conversation Flow

1. **Initial Greeting**: Introduces the vacation package and destination
2. **Guest Information**: Collects zip code and number of guests
3. **Date Selection**: Asks for preferred month/week, shows available date ranges
4. **Tour Selection**: Presents available tour dates and times
5. **Accommodation Selection**: Presents available properties and room types
6. **Booking Summary**: Provides a complete summary of all selections

## Sample Data

Sample JSON data for testing is available in `datasource/SampleData/`:
- `availabilities.json`: Tour date and time availability
- `accommodations.json`: Available accommodations and room types
- `PackageDetails.json`: Vacation package information

## Dependencies

- semantic-kernel>=0.9.1
- openai>=1.24.0
- python-dotenv>=1.0.0
- fastapi>=0.111.0
- uvicorn[standard]>=0.29.0

## License

[Specify your license here]
