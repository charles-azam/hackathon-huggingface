from io import BytesIO
from time import sleep
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool
import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from smolagents import CodeAgent, tool
from smolagents.agents import ActionStep

# Load environment variables
load_dotenv()

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--window-size=1000,1350")
chrome_options.add_argument("--disable-pdf-viewer")
chrome_options.add_argument("--window-position=0,0")

# Initialize the browser
driver = helium.start_chrome(headless=False, options=chrome_options)

# Set up screenshot callback
def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    driver = helium.get_driver()
    current_step = memory_step.step_number
    if driver is not None:
        for previous_memory_step in agent.memory.steps:  # Remove previous screenshots for lean processing
            if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
                previous_memory_step.observations_images = None
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"Captured a browser screenshot: {image.size} pixels")
        memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists

    # Update observations with current URL
    url_info = f"Current url: {driver.current_url}"
    memory_step.observations = (
        url_info if memory_step.observations is None else memory_step.observations + "\n" + url_info
    )

@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    Args:
        text: The text to search for
        nth_result: Which occurrence to jump to (default: 1)
    """
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(f"Match n°{nth_result} not found (only {len(elements)} matches found)")
    result = f"Found {len(elements)} matches for '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focused on element {nth_result} of {len(elements)}"
    return result

@tool
def go_back() -> None:
    """Goes back to previous page."""
    driver.back()

@tool
def close_popups() -> str:
    """
    Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows!
    This does not work on cookie consent banners.
    """
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Initialize the model
model_id = "anthropic/claude-sonnet-4-20250514"  # You can change this to your preferred VLM model
model = LiteLLMModel(model_id)

# Create the agent
agent = CodeAgent(
    tools=[go_back, close_popups, search_item_ctrl_f],
    model=model,
    additional_authorized_imports=["helium"],
    step_callbacks=[save_screenshot],
    max_steps=20,
    verbosity_level=2,
)

# Import helium for the agent
agent.python_executor("from helium import *")

airbnb_instructions = """
You can use helium to access Airbnb and perform research. The browser is already set up.
We've already ran "from helium import *"

To navigate to Airbnb:
```py
go_to('airbnb.com')
```

You can search for properties by:
1. Using the search bar
2. Clicking on filters
3. Scrolling through results

To interact with elements:
```py
# Click on text
click("Search")

# Click on links
click(Link("Explore"))

# Click on buttons
click(Button("Show more"))
```

To scroll through results:
```py
scroll_down(num_pixels=1200)  # Scroll one viewport down
scroll_up(num_pixels=1200)    # Scroll one viewport up
```

To handle popups and modals:
```py
close_popups()  # Use this for any popup windows
```

To check for elements:
```py
if Text('Accept cookies?').exists():
    click('I accept')
```

Important guidelines:
1. Never try to log in or create an account
2. Don't click on "Book now" or similar booking buttons
3. Focus on gathering information about properties, prices, and locations
4. Take screenshots after each significant action to track progress
5. Use the search_item_ctrl_f tool to find specific text on the page
"""

# Example research request
research_request = """
Please research Airbnb properties in Paris, France. Look for:
1. Average price range for a 2-bedroom apartment
2. Popular neighborhoods
3. Common amenities offered
"""

agent_output = agent.run(research_request + airbnb_instructions)
print("Final output:")
print(agent_output) 