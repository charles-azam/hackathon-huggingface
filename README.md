# Travel Planning Agent

An AI-powered travel planning system that generates personalized travel packages with flights, accommodations, and activities.

## Features

- **Multi-budget Packages**: Generates three different budget tiers (low, medium, high) for each trip
- **Comprehensive Planning**: Includes flights, accommodations, and activities
- **Real-time Research**: Uses web search to find current prices and availability
- **Structured Output**: Returns well-formatted travel packages with all necessary details

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/travel-planning-agent.git
cd travel-planning-agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from loulou.travel_agent import run_travel_agent

# Generate travel plans
plans = run_travel_agent(
    n_travelers=2,
    arrival_date="2025-06-16",
    departure_date="2025-06-26",
    departure="Paris",
    arrival="Tokyo"
)

```
## Technical description



## Technical description
![archi.webp](archi.webp)

Technologies:
- smolagents
- anthropic
- huggingface
- browser-use

In this project we have 4 agents:
- a flight agent
- a housing agent
- an activities agent
- a structure agent

**Flight and housing agent**:
Using smolagents and selenium was extremely long. So what we used browser-use to get started and once we got to the good url with the search result, we would use a callback to stop browser-use and start smolagents with selenium.

For the activities agent, we used a classic smolagent along with duckduckgo.

In the end, we just wanted to get a structured output for the back which was extremely hard to do with a simple llm called so we ended up using smolagents to get a structured output with all the results



## Project Structure

```
.
├── docs/
│   └── travel_agent.py      # Main travel planning agent
├── src/
│   └── loulou/
│       ├── activities_agent.py  # Activities recommendation agent
│       ├── browser_use_tools.py # Browser automation tools
│       ├── classes.py           # Pydantic models
│       └── smolagents_tool.py   # Custom smolagents tools
└── requirements.txt
```
## Components

### Travel Agent
The main agent that coordinates the entire travel planning process:
- Researches flights and accommodations
- Generates activity recommendations
- Creates comprehensive travel packages

### Activities Agent
Specialized agent for recommending activities:
- Suggests activities for different budget levels
- Includes free activities and must-see attractions
- Provides booking links and costs

### Data Models
Pydantic models for structured data:
- `Packages`: Collection of travel packages
- `Package`: Individual travel package
- `BudgetBreakdown`: Cost breakdown
- `Flights`: Flight information
- `Hotel`: Accommodation details
- `Activity`: Activity information

## Dependencies

- smolagents: For AI agent functionality
- pydantic: For data validation
- langchain: For structured output
- selenium: For web automation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.