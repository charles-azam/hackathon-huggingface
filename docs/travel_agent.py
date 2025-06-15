import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel,InferenceClientModel, OpenAIServerModel
from langchain_community.document_loaders import WikipediaLoader
from smolagents import tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import helium

# import agents
from loulou.price_research_agent import find_three_candidates_on_website


haiku = 'anthropic/claude-3-5-haiku-20241022'
sonnet = 'anthropic/claude-sonnet-4-20250514'


# define all agents and tools
# flight_agent = 
# airbnb_agent = 
# activities_agent = 
# managed_agents = [flight_agent, airbnb_agent, activities_agent]

# tools
airbnb_search = tool(find_three_candidates_on_website)
tools_list = [airbnb_search]
# final checks

# manager agent
manager_agent = CodeAgent(
    model= LiteLLMModel(model_id = sonnet, api_key=os.environ['CLAUDE_API']),
    tools=tools_list,
    # managed_agents=managed_agents,
    additional_authorized_imports=[],
    planning_interval=5,
    verbosity_level=2,
    # final_answer_checks=[check_reasoning_and_plot],
    max_steps=15,
)

system_prompt = '''
You are a helpful assistant who's mission is to plan travels for users. 
You can manage 3 agents: 
a flight agent that can find flights on google flights and outputs the dates, budget and url for booking,
an airbnb agent that can find houses on airbnb and outputs the dates budget and url for booking purposes
an activities agent that can propose activities and outputs a list of activities

Take the inputs of the three agents and combine the outputs into 3 differents travel plans with 3 budget tiers: low cost, medium cost and high cost
all agents will outputs a list of options which differents prices, chose one of them in each 
your output should follow the template:
Budget tier = [budget tier]: 
Dates = [arrival date, departure date]
budget = [cost of chosen flight + cost of housing + estimation of activities cost]
flight = [url of chosen flight]
airbnb = [url of chosen house]

'''

# hardcoded outputs
hardcoded_system_prompt = '''
You are a helpful assistant who's mission is to plan travels for users. 
You have 3 tools: 
a flight agent that can find flights on google flights and outputs the dates, budget and url for booking,
an airbnb search toolqa that can find houses on airbnb and outputs the dates budget and url for booking purposes
an activities agent that can propose activities and outputs a list of activities

Take the inputs of the three agents and combine the outputs into 3 differents travel plans with 3 budget tiers: low cost, medium cost and high cost
your output should follow the template:
Budget tier = [budget tier]: 
Dates = [arrival date, departure date]
budget = [cost of chosen flight + cost of housing + estimation of activities cost]
flight = [url of chosen flight]
airbnb = [url of chosen house]

'''

number_of_people = 2
departure = 'Paris'
arrival = 'Barcelona'
dates = '24/06/2025 to 27/06/2025'
budget = 500

task = f'Propose a travel plan for {number_of_people} persons from {departure} to {arrival} for the following dates {dates} under the following budget {budget} euros'

manager_agent.run(hardcoded_system_prompt + task)