import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel,InferenceClientModel, OpenAIServerModel
from langchain_community.document_loaders import WikipediaLoader
from smolagents import tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import helium

# import agents
from loulou.smolagents_tool import research_airbnb, research_google_travel



def run_travel_agent(n_travelers: int, arrival_date: str, departure_date: str,
                      departure: str,arrival: str, budget: float
) -> str:
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
        budget (float): Total budget in euros.

    Returns:
        str: A formatted travel plan proposal including three budget-tiered itineraries
             with URLs for flights and accommodations.
    """
    # tools
    tools_list = [research_airbnb, research_google_travel]

    sonnet = 'anthropic/claude-sonnet-4-20250514'

    # manager agent
    manager_agent = CodeAgent(
        model= LiteLLMModel(model_id = sonnet, api_key=os.environ['ANTHROPIC_API_KEY']),
        tools=tools_list,
        additional_authorized_imports=[],
        planning_interval=5,
        verbosity_level=2,
        # final_answer_checks=[check_reasoning_and_plot],
        max_steps=15,
    )

    system_prompt = '''
        You are a helpful assistant who's mission is to plan travels for users. 
        You have 3 tools: 
        a research_google_travel that can find flights on google flights and outputs the dates, budget and url for booking,
        an research_airbnb tool that can find houses on airbnb and outputs the dates budget and url for booking purposes
        an activities_search that can look for activities  and outputs a list of activities with their corresponding price and url

        The 3 tools outputs follow this format:
        - low:
            - link:
            - price:
            - description:
        - medium:
            - link:
            - price:
            - description:
        - high:
            - link:
            - price:
            - description:

        Take the inputs of the three agents and combine the outputs into 3 differents travel plans with 3 budget tiers: low cost, medium cost and high cost
        your output should follow the template:

        '''
    output_template = '''
        Budget tier = [budget tier]: 
        Dates = [arrival date, departure date]
        budget = [cost of chosen flight + cost of housing + estimation of activities cost]
        flight = [url of chosen flight]
        airbnb = [url of chosen house]

        '''
    
    task = f'Propose a travel plan for {n_travelers} persons from {departure} to {arrival} for the following dates [{arrival_date} to {departure_date}] under the following budget {budget} euros'
    output = manager_agent.run(system_prompt + output_template + task)
    return output
