import os
from pydantic_ai import Agent
from loulou.smolagents_tool import research_airbnb, research_google_travel
from loulou.classes import Packages


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
    output_airbnb = research_airbnb(objective_housing)
    output_flight = research_google_travel(objective_flight)

    # Initialize the agent with our Packages model
    agent = Agent('claude-sonnet-4-20250514', output_type=Packages)

    # Create the prompt
    prompt = f"""
    Create a travel plan with three different budget tiers (low, medium, high) based on the following research:

    Flight Information:
    {output_flight}

    Accommodation Information:
    {output_airbnb}

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
    """

    # Run the agent
    result = agent.run_sync(prompt)
    print(f"Usage: {result.usage()}")
    return result.output


if __name__ == "__main__":
    plans = run_travel_agent(
        n_travelers=2,
        arrival_date="2025-06-16",
        departure_date="2025-06-26",
        departure="Paris",
        arrival="Barcelona"
    )
    print("\nGenerated Travel Plans:")
    for package in plans.packages:
        print(f"\n=== {package.title} ===")
        print(f"Duration: {package.duration}")
        print(f"Total Price: ${package.price}")
        print("\nBudget Breakdown:")
        print(f"- Flights: ${package.budgetBreakdown.flights}")
        print(f"- Hotels: ${package.budgetBreakdown.hotels}")
        print(f"- Activities: ${package.budgetBreakdown.activities}")
        print(f"- Food: ${package.budgetBreakdown.food}")