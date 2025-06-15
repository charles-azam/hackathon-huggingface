# !pip install smolagents[litellm]
from smolagents import CodeAgent, LiteLLMModel
from smolagents import WebSearchTool
from smolagents import DuckDuckGoSearchTool
import os
from loulou.browser_use_tools import TASK_EXAMPLE, ChatAnthropic


def run_activities_agent(task: str):
    """
    Run the activities agent to recommend activities for a holiday trip.
    
    Args:
        task (str): The task to recommend activities for a holiday trip.
        
    Returns:
        str: The result of the activities agent.
    """

    activities_instructions = """
    You are a travel planning assistant. Your task is to recommend activities for a holiday trip.

    Please divide recommendations into different budget levels and make sure all suggestions are appropriate for the group size.

    ### Instructions:

    1. For **each budget level** — `"low"`, `"medium"`, and `"high"` — suggest **5 diverse activities**. Each activity must include:
        - A short title
        - Description
        - Approximate cost (total, for the group)
        - Category (e.g., "outdoor", "cultural", "food", etc.)
        - The link to book or learn more about the activity (if available)

    2. Provide a separate list of at least **5 free activities** (e.g., landmarks, public attractions, scenic spots). These should be things **not to miss**.

    3. Return the result as a JSON object, structured like this: 
    {
    "destination": "string",
    "num_people": number,
    "recommendations": {
        "low": [
        {
            "title": "string",
            "description": "string",
            "cost": number,
            "category": "string",
            "link": "string"
        }
        ],
        "medium": [...],
        "high": [...]
    },
    "free_activities": [
        {
        "title": "string",
        "description": "string",
        "category": "string",
        "link": "string"
        }
    ]
    }
    """

    research_request = f"""
    The original task is to : {task}
    """

    # Initialize the model and agent
    model = LiteLLMModel("claude-sonnet-4-20250514")
    agent = CodeAgent(
        model=model,
        tools=[DuckDuckGoSearchTool()],
        additional_authorized_imports=["*"]
    )
        
    # Run the agent and get the response
    response = agent.run(research_request + activities_instructions)
    
    # Handle the response based on its type
    if hasattr(response, 'content'):
        return response.content
    elif isinstance(response, str):
        return response
    else:
        return str(response)


if __name__ == "__main__":
    result = run_activities_agent("Plan activities for a family trip to Tokyo")
    print(result)
