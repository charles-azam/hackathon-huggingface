# !pip install smolagents[litellm]
from smolagents import CodeAgent, LiteLLMModel
from smolagents import WebSearchTool
from smolagents import DuckDuckGoSearchTool
from smolagents import PromptTemplates, PlanningPromptTemplate, ManagedAgentPromptTemplate, FinalAnswerPromptTemplate
import os
model = LiteLLMModel(model_id="anthropic/claude-3-5-sonnet-latest", api_key=os.getenv("ANTHROPIC_API_KEY"))


TEMPLATE = """
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
{{
  "destination": "string",
  "num_people": number,
  "recommendations": {{
    "low": [
      {{
        "title": "string",
        "description": "string",
        "cost": number,
        "category": "string",
        "link": "string"
      }}
    ],
    "medium": [...],
    "high": [...]
  }},
  "free_activities": [
    {{
      "title": "string",
      "description": "string",
      "category": "string",
      "link": "string"
    }}
  ]
}}
"""
# 1. Define individual template components
system_prompt = TEMPLATE


# 1. Planning Template - Controls execution flow
planning_template = PlanningPromptTemplate(
    plan="""1. Analyze destination and group size
2. Generate 5 activities per budget tier
3. Curate 5 free attractions
4. Structure as valid JSON""",
    
    update_plan_pre_messages="""Check if current response contains:
- All required budget tiers
- Proper cost calculations
- Valid activity links""",
    
    update_plan_post_messages="""Verify JSON structure matches:
{{
  "destination": "...",
  "num_people": ...,
  "recommendations": {{"low": [...], ...}},
  "free_activities": [...]
}}"""
)

# 2. Managed Agent Template - Handles core logic
managed_agent_template = ManagedAgentPromptTemplate(
    task="""Follow these instructions strictly:
{template_instructions}
    
Main Constraints:
- Group size:
- Destination: 
- Budget tiers: low/medium/high""",
    
    report="""Generated {total_activities} activities across budgets
Included {free_activities_count} free attractions
JSON validation: {validation_status}"""
).format(template_instructions=TEMPLATE)  # Inject your template here

# 3. Final Answer Template - Ensures output quality
final_answer_template = FinalAnswerPromptTemplate(
    pre_messages="""Validate response contains:
1. 5 activities per budget level
2. Cost calculations for {num_people} people
3. At least 3 different categories
4. Working booking links""",
    
    post_messages="""Format final output as: {required_structure}""")


agent_templates = PromptTemplates(
    system_prompt=system_prompt,
    planning=planning_template,
    managed_agent=managed_agent_template,
    final_answer=final_answer_template
)

# Function to run the agent with given inputs
agent = CodeAgent(
    model=model,
    tools=[DuckDuckGoSearchTool()],
    prompt_templates=agent_templates,
    add_base_tools=False,
    additional_authorized_imports=["json"])

    
response = agent.run("I want to go to Barcelona with 4 people")
print(response)
