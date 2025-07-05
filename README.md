# AI Vacation Package Sales Agent

A conversational AI agent for selling vacation packages using Microsoft's Semantic Kernel, Azure OpenAI, and FastAPI. This agent guides potential customers through the vacation booking process with a natural, step-by-step conversation flow.

## Project Overview

This project implements an AI-powered vacation sales agent that helps users book vacation packages by:

1. Collecting user preferences (destination, dates, number of guests)
2. Presenting available date ranges and tour options
3. Guiding users through accommodation selection
4. Providing a complete booking summary

The agent uses a sequential, conversational approach to avoid overwhelming users with too many options at once.

## Key Features

- **Natural Conversational Flow**: Step-by-step guidance through the booking process
- **Intelligent Date Handling**: Normalizes dates to ensure consistent year references (2025)
- **Modular Architecture**: Clean separation of concerns with specialized tools
- **Strong Data Validation**: Pydantic models ensure data integrity
- **Session Management**: Session-based agent caching with TTL
- **Web Interface**: User-friendly chat UI

## Project Structure

```
.
├── agent_garden/       # Agent lifecycle management and caching
├── agents/             # Agent implementations with conversation logic
│   └── vacation_agent.py  # Main vacation booking agent implementation
├── controllers/        # FastAPI controllers for web endpoints
├── models/             # Pydantic data models for validation
│   ├── availability_models.py  # Models for tour availability
│   ├── accommodation_models.py # Models for accommodation options
│   └── request_models.py       # API request/response models
├── static/             # Frontend assets and chat UI
├── system/             # System configuration and environment settings
├── tools/              # Specialized agent tools
│   ├── availability_tools.py   # Tools for managing tour availability
│   ├── accommodation_tools.py  # Tools for accommodation selection
│   └── package_tools.py        # Tools for package details and validation
└── SampleData/         # Sample JSON data for testing
    ├── availabilities.json     # Tour date and time availability
    ├── accommodations.json     # Available accommodations and room types
    └── PackageDetails.json     # Vacation package information
```

## Technical Implementation

### Core Components

- **Semantic Kernel**: Provides the foundation for building AI agents with tool-calling capabilities
- **Azure OpenAI Integration**: Powers the conversational AI capabilities
- **FastAPI**: Handles HTTP requests and serves the web interface
- **Pydantic Models**: Ensures data validation and type safety

### Specialized Tools

- **AvailabilityDetails**: Manages tour date and time availability
- **AccommodationDetails**: Handles accommodation and room type selection
- **PackageDetails**: Provides package information and validation

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
   # Windows
   .venv\Scripts\activate
   # Unix/MacOS
   source .venv/bin/activate
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
   ```

5. Run the application
   ```bash
   python main.py
   ```

6. Access the chat interface at `http://localhost:8081`

## Conversation Flow

The agent follows a carefully designed conversation flow:

1. **Initial Greeting**: Introduces the vacation package and destination
2. **Guest Information**: Collects zip code and number of guests
3. **Date Selection**: 
   - Asks for preferred month and week
   - Shows available date ranges
4. **Tour Selection**: 
   - First presents available tour dates for the selected range
   - Then presents available times for the selected date
5. **Accommodation Selection**:
   - First presents available accommodation properties
   - Then presents room types for the selected property
6. **Booking Summary**: Provides a complete summary of all selections

## Recent Improvements

- Fixed date filtering logic to ensure consistent year references (2025)
- Improved conversational flow with sequential option presentation
- Enhanced accommodation selection process with separate property and room type steps
- Added data validation to ensure proper parsing of JSON data

## Dependencies

- semantic-kernel>=0.9.1
- openai>=1.24.0
- python-dotenv>=1.0.0
- fastapi>=0.111.0
- uvicorn[standard]>=0.29.0

## License

[Specify your license here]
