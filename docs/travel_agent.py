import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, tool
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from loulou.smolagents_tool import research_airbnb, research_google_travel
from loulou.classes import Packages
import json
from loulou.activities_agent import run_activities_agent

@tool
def validate_package_json(json_str: str) -> bool:
    """
    This tool is used to validate the output of the agent.
    
    Args:
        json_str (str): The JSON string to validate.
        
    Returns:
        bool: True if the JSON string can be converted to a valid Package object, False otherwise.
    """
    try:
        data = json.loads(json_str)
        Packages(**data)
        return True
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False


def run_travel_agent(n_travelers: int, arrival_date: str, departure_date: str,
                    departure: str, arrival: str) -> Packages:
    """
    Generates personalized travel plans for a group of travelers using an AI-powered planning agent.

    This function utilizes a CodeAgent configured with the Claude Sonnet model and equipped with
    a research tool to search for accommodations (e.g., via Airbnb). It builds a travel plan by
    gathering flight, housing, and activity suggestions, and combines them into three budget tiers:
    low cost, medium cost, and high cost.

    Parameters:
        n_travelers (int): Number of travelers.
        arrival_date (str): Planned arrival date (e.g., "2025-07-01").
        departure_date (str): Planned departure date (e.g., "2025-07-10").
        departure (str): Departure location (e.g., "New York").
        arrival (str): Destination location (e.g., "Paris").

    Returns:
        Packages: A structured travel plan proposal including three budget-tiered itineraries
                  with URLs for flights and accommodations.
    """
    # Get research results
    objective_flight = f'search for a flight for {n_travelers} persons from {departure} to {arrival} for the following dates [{arrival_date} to {departure_date}]'
    objective_housing = f'search for housing for {n_travelers} persons from {departure} to {arrival} for the following dates [{arrival_date} to {departure_date}]'
    objective_activities = f'search for activities for {n_travelers} persons from {departure} to {arrival} for the following dates [{arrival_date} to {departure_date}]'
    activities_info = run_activities_agent(objective_activities)
    with open("activities_info.txt", "w") as f:
        f.write(activities_info)
    output_airbnb = research_airbnb(objective_housing)
    with open("output_airbnb.txt", "w") as f:
        f.write(output_airbnb)
    output_flight = research_google_travel(objective_flight)
    with open("output_flight.txt", "w") as f:
        f.write(output_flight)

    # Initialize the agent with Claude model
    model = LiteLLMModel("claude-sonnet-4-20250514")
    agent = CodeAgent(model=model, tools=[validate_package_json], additional_authorized_imports=["*"])

    # Create the parser and prompt template
    parser = PydanticOutputParser(pydantic_object=Packages)
    prompt_template = PromptTemplate(
        template="""
        Create a travel plan with three different budget tiers (low, medium, high) based on the following research:

        Flight Information:
        {flight_info}

        Accommodation Information:
        {accommodation_info}

        Activities Information:
        {activities_info}

        Requirements:
        - Number of travelers: {n_travelers}
        - Dates: {arrival_date} to {departure_date}
        - From: {departure}
        - To: {arrival}

        Create three packages with the following structure:

        1. Low budget package:
           - Focus on cost-effective options while maintaining basic comfort
           - Use budget airlines and hostels/guesthouses
           - Include free or low-cost activities
           - Total price should be under 1000 euros per person

        2. Medium budget package:
           - Balance between cost and comfort
           - Use regular airlines and 3-star hotels
           - Mix of free and paid activities
           - Total price should be between 1000-2000 euros per person

        3. High budget package:
           - Premium options with luxury amenities
           - Use major airlines and 4-5 star hotels
           - Include premium activities and experiences
           - Total price should be over 2000 euros per person

        For each package, ensure:
        - All prices are in euros
        - Flight times are realistic
        - Hotel ratings are between 0-5 stars
        - URLs are valid and accessible
        - Activities are appropriate for the budget level
        - Total price matches the sum of all components

        If any information is missing from the research, make reasonable assumptions based on typical prices and options for the destination.
        
        {format_instructions}
        
        You must return a valid pydantic object at all cost and nothing else.
        
        Use the validate_package_json tool to validate the output. Give your final answer only if it passes the validation.
        """,
        input_variables=["flight_info", "accommodation_info", "activities_info", "n_travelers", 
                        "arrival_date", "departure_date", "departure", "arrival"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    # Format the prompt
    prompt = prompt_template.format(
        flight_info=output_flight,
        accommodation_info=output_airbnb,
        activities_info=activities_info,
        n_travelers=n_travelers,
        arrival_date=arrival_date,
        departure_date=departure_date,
        departure=departure,
        arrival=arrival
    )

    # Run the agent
    result = agent.run(prompt)
    with open("result.txt", "w") as f:
        f.write(str(result))
    return Packages.model_validate_json(result)


if __name__ == "__main__":
    plans = run_travel_agent(
        n_travelers=2,
        arrival_date="2025-06-16",
        departure_date="2025-06-26",
        departure="Paris",
        arrival="Tokyo"
    )
