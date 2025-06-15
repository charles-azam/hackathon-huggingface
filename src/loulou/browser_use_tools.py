import asyncio
from dotenv import load_dotenv
from pathlib import Path
from typing import Any
from browser_use import Agent
from langchain_anthropic import ChatAnthropic
from loulou.common import HUGGING_FACE_PATH


SAVE_DATA_PATH = HUGGING_FACE_PATH / "data" / "browser_use_test"
SAVE_DATA_PATH.mkdir(parents=True, exist_ok=True)


TASK_EXAMPLE = """
GO to airbnb, search for a 2 bedroom apartment in the center of Barcelona for 2 people for 10 nights from 16/06/2025.
"""

def run_get_url_agent(task: str = TASK_EXAMPLE, llm: ChatAnthropic = ChatAnthropic(model="claude-sonnet-4-20250514"), url_contains: str = "homes") -> str:
    """
    Synchronous function that runs the Airbnb research and returns the results including screenshots.
    """
    URL_SAVE_PATH = SAVE_DATA_PATH / "url_contains.url"
    
    async def my_step_hook(agent: Agent):
        # Get the current page and URL
        page = await agent.browser_session.get_current_page()
        current_url = page.url
        
        # Check if we've hit a URL containing 'homes'
        if url_contains in current_url:
            print(f"Found listings page at: {current_url}")
            # Save the page content
            
            URL_SAVE_PATH.write_text(current_url)
            print(f"Saved listings page content to {URL_SAVE_PATH}")
            agent.stop()
            
    async def async_research():
        agent = Agent(
            task=task,
            llm=llm,
        )
        await agent.run(on_step_start=my_step_hook)
    
    output = asyncio.run(async_research())
    return URL_SAVE_PATH.read_text()




if __name__ == "__main__":
    # Example usage
    results = run_get_url_agent()
    print(results)
