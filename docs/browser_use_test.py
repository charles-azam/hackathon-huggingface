import asyncio
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Any
from browser_use import Agent
from langchain_anthropic import ChatAnthropic
from loulou.common import HUGGING_FACE_PATH


load_dotenv()

SAVE_DATA_PATH = HUGGING_FACE_PATH / "data" / "browser_use_test"
SAVE_DATA_PATH.mkdir(parents=True, exist_ok=True)


async def my_step_hook(agent: Agent):
    # Get the current page and URL
    page = await agent.browser_session.get_current_page()
    current_url = page.url
    
    # Check if we've hit a URL containing 'homes'
    if 'homes' in current_url:
        print(f"Found listings page at: {current_url}")
        # Save the page content
        
        (SAVE_DATA_PATH / 'airbnb_listings.html').write_text(await page.content())
        (SAVE_DATA_PATH / 'airbnb_listings.url').write_text(current_url)
        print("Saved listings page content to airbnb_listings.html")
        agent.stop()


def run_airbnb_research() -> Dict[str, Any]:
    """
    Synchronous function that runs the Airbnb research and returns the results including screenshots.
    Returns a dictionary containing:
    - screenshots: List of screenshot paths
    - urls: List of visited URLs
    - actions: List of executed actions
    - content: Extracted content
    - errors: Any errors that occurred
    """
    async def async_research():
        agent = Agent(
            task="""
GO to airbnb, search for a 2 bedroom apartment in the center of Barcelona for 2 people for 10 nights from 16/06/2025.

Stop as soon as you hit the page where all of the listings are shown.
""",
            llm=ChatAnthropic(model="claude-sonnet-4-20250514"),
        )
        history = await agent.run(on_step_start=my_step_hook)
        return {
            "screenshots": history.screenshots(),
            "urls": history.urls(),
            "actions": history.action_names(),
            "content": history.extracted_content(),
            "errors": history.errors(),
            "model_actions": history.model_actions()
        }

    # Run the async function and return its results
    output = asyncio.run(async_research())
    print(output)
    return output


if __name__ == "__main__":
    # Example usage
    results = run_airbnb_research()
