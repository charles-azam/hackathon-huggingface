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
from loulou.browser_use_tools import run_get_url_agent, TASK_EXAMPLE, ChatAnthropic


def run_research_agent(task: str = TASK_EXAMPLE, website_name: str = "airbnb", url_contains: str = "homes", llm: ChatAnthropic = ChatAnthropic(model="claude-sonnet-4-20250514")) -> str:
    if "flight" in website_name:
        return """
Final output:
- low:
    - link: https://www.google.com/travel/flights/search?tfs=CBwQAhpKEgoyMDI1LTA2LTE2IiAKA09SWRIKMjAyNS0wNi0xNhoDQkNOKgJUTzIENDc1MGoMCAISCC9tLzA1cXRqcgwIAxIIL20vMDFmNjIaKBIKMjAyNS0wNi0yNmoMCAMSCC9tLzAxZjYycgwIAhIIL20vMDVxdGpAAUgBcAGCAQsI____________AZgBAQ&tfu=CmxDalJJYmtnNGFrOXpkVmRyUWtsQlRqWlBZV2RDUnkwdExTMHRMUzB0TFhkbWFHVTBNVUZCUVVGQlIyaFBkSFZyUjNjNFlqSkJFZ1pVVHpRM05UQWFDZ2lnVVJBQ0dnTkZWVkk0SEhEeVhRPT0SAggAIgA
    - price: 104€
    - description: Transavia direct flight Paris-Barcelona, 2h duration, round trip with multiple time options
- medium:
    - link: https://www.google.com/travel/flights/search?tfs=CBwQAhpKEgoyMDI1LTA2LTE2IiAKA09SWRIKMjAyNS0wNi0xNhoDQkNOKgJUTzIENDgwMGoMCAISCC9tLzA1cXRqcgwIAxIIL20vMDFmNjIaKBIKMjAyNS0wNi0yNmoMCAMSCC9tLzAxZjYycgwIAhIIL20vMDVxdGpAAUgBcAGCAQsI____________AZgBAQ&tfu=CmxDalJJVXpGaGVUWTNkV3RDYlc5QlQwOXVUbmRDUnkwdExTMHRMUzB0TFhkaVltWjVORUZCUVVGQlIyaFBkSFpaUzNGMGVWZEJFZ1pVVHpRNE1EQWFDZ2pBVnhBQ0dnTkZWVkk0SEhDT1pRPT0SAggAIgMKATA
    - price: 112€
    - description: Transavia direct flight Paris-Barcelona, 2h duration, round trip with multiple departure times
- high:
    - link: https://www.google.com/travel/flights/search?tfs=CBwQAhpKEgoyMDI1LTA2LTE2IiAKA09SWRIKMjAyNS0wNi0xNhoDQkNOKgJWWTIEODAxM2oMCAISCC9tLzA1cXRqcgwIAxIIL20vMDFmNjIaKBIKMjAyNS0wNi0yNmoMCAMSCC9tLzAxZjYycgwIAhIIL20vMDVxdGpAAUgBcAGCAQsI____________AZgBAQ&tfu=CmxDalJJWTE5T2RVbDVka3gzWkZGQlUwMUJhbWRDUnkwdExTMHRMUzB0WldwamEzQXlOa0ZCUVVGQlIyaFBkSFJOUkVRdGNXVkJFZ1pXV1Rnd01UTWFDZ2p1ZVJBQ0dnTkZWVkk0SEhEb2pBRT0SAggAIgA
    - price: 156€
    - description: Vueling direct flight Paris-Barcelona, 2h duration, round trip with premium service options
- low:
    - link: https://www.google.com/travel/flights/search?tfs=CBwQAhpKEgoyMDI1LTA2LTE2IiAKA09SWRIKMjAyNS0wNi0xNhoDQkNOKgJUTzIENDc1MGoMCAISCC9tLzA1cXRqcgwIAxIIL20vMDFmNjIaKBIKMjAyNS0wNi0yNmoMCAMSCC9tLzAxZjYycgwIAhIIL20vMDVxdGpAAUgBcAGCAQsI____________AZgBAQ&tfu=CmxDalJJYmtnNGFrOXpkVmRyUWtsQlRqWlBZV2RDUnkwdExTMHRMUzB0TFhkbWFHVTBNVUZCUVVGQlIyaFBkSFZyUjNjNFlqSkJFZ1pVVHpRM05UQWFDZ2lnVVJBQ0dnTkZWVkk0SEhEeVhRPT0SAggAIgA
    - price: 104€
    - description: Transavia direct flight Paris-Barcelona, 2h duration, round trip with multiple time options
- medium:
    - link: https://www.google.com/travel/flights/search?tfs=CBwQAhpKEgoyMDI1LTA2LTE2IiAKA09SWRIKMjAyNS0wNi0xNhoDQkNOKgJUTzIENDgwMGoMCAISCC9tLzA1cXRqcgwIAxIIL20vMDFmNjIaKBIKMjAyNS0wNi0yNmoMCAMSCC9tLzAxZjYycgwIAhIIL20vMDVxdGpAAUgBcAGCAQsI____________AZgBAQ&tfu=CmxDalJJVXpGaGVUWTNkV3RDYlc5QlQwOXVUbmRDUnkwdExTMHRMUzB0TFhkaVltWjVORUZCUVVGQlIyaFBkSFpaUzNGMGVWZEJFZ1pVVHpRNE1EQWFDZ2pBVnhBQ0dnTkZWVkk0SEhDT1pRPT0SAggAIgMKATA
    - price: 112€
    - description: Transavia direct flight Paris-Barcelona, 2h duration, round trip with multiple departure times
- high:
    - link: https://www.google.com/travel/flights/search?tfs=CBwQAhpKEgoyMDI1LTA2LTE2IiAKA09SWRIKMjAyNS0wNi0xNhoDQkNOKgJWWTIEODAxM2oMCAISCC9tLzA1cXRqcgwIAxIIL20vMDFmNjIaKBIKMjAyNS0wNi0yNmoMCAMSCC9tLzAxZjYycgwIAhIIL20vMDVxdGpAAUgBcAGCAQsI____________AZgBAQ&tfu=CmxDalJJWTE5T2RVbDVka3gzWkZGQlUwMUJhbWRDUnkwdExTMHRMUzB0WldwamEzQXlOa0ZCUVVGQlIyaFBkSFJOUkVRdGNXVkJFZ1pXV1Rnd01UTWFDZ2p1ZVJBQ0dnTkZWVkk0SEhEb2pBRT0SAggAIgA
    - price: 156€
    - description: Vueling direct flight Paris-Barcelona, 2h duration, round trip with premium service options

"""
    if website_name == "airbnb":
        return """
Final output:
Thought: Perfect! I can see the pricing information for the high budget option. It's 82€ per night with a total of 959€ for 10 nights. This is a modern renovated studio with excellent location on Avenida Paralel. 

Now I have all three budget options:

1. LOW budget: Carolina's place - 77€ per night (804€ total)
2. MEDIUM budget: Arief's place - 77€ per night (771€ total) 
3. HIGH budget: Studio with balcony - 82€ per night (959€ total)

Actually, looking at the prices, I need to adjust the categorization based on the total costs:
- LOW: 771€ total (Arief's place)
- MEDIUM: 804€ total (Carolina's place)
- HIGH: 959€ total (Studio with balcony)

Let me finalize the information:

Code:
```py
# Store the high budget information
high_budget_info = {
    'link': high_budget_url,
    'price': '82€ per night (959€ total)',
    'description': 'Joli studio avec balcon ! Emplacement idéal - Modern renovated studio with balcony, excellent location on Avenida Paralel, close to port and Rambla'
}

# Final categorization based on total costs
final_results = {
    'low': {
        'link': 'https://www.airbnb.fr/rooms/1204325388447050009?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=1965799709&source_impression_id=p3_1749988526_P3savPxDcmUDopEC&previous_page_section_name=1000&federated_search_id=f3f82737-9c10-4867-a55a-ecaf22f2f7a3',
        'price': '77€ per night (771€ total)',
        'description': 'Chambre dans le centre avec air conditionné - Room in apartment with air conditioning in the center of Barcelona'
    },
    'medium': {
        'link': 'https://www.airbnb.fr/rooms/1409980769386304321?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=2155293160&source_impression_id=p3_1749988662_P3PTujRArrwsVOAQ&previous_page_section_name=1000&federated_search_id=0c23fe5d-6bc0-484d-bec9-e8f414f510dd',
        'price': '77€ per night (804€ total)',
        'description': 'Chambre privée pour 2 à Borne - Private room for 2 travelers with shared bathroom in apartment in Born'
    },
    'high': high_budget_info
}

print("Final results collected!")
```<end_code>
Calling tools:
[{'id': 'call_21', 'type': 'function', 'function': {'name': 'python_interpreter', 'arguments': '# Store the high budget information\nhigh_budget_info = {\n    \'link\': high_budget_url,\n    \'price\': \'82€ per night (959€ total)\',\n    \'description\': \'Joli studio avec balcon ! Emplacement idéal - Modern renovated studio with balcony, excellent location on Avenida Paralel, close to port and Rambla\'\n}\n\n# Final categorization based on total costs\nfinal_results = {\n    \'low\': {\n        \'link\': \'https://www.airbnb.fr/rooms/1204325388447050009?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=1965799709&source_impression_id=p3_1749988526_P3savPxDcmUDopEC&previous_page_section_name=1000&federated_search_id=f3f82737-9c10-4867-a55a-ecaf22f2f7a3\',\n        \'price\': \'77€ per night (771€ total)\',\n        \'description\': \'Chambre dans le centre avec air conditionné - Room in apartment with air conditioning in the center of Barcelona\'\n    },\n    \'medium\': {\n        \'link\': \'https://www.airbnb.fr/rooms/1409980769386304321?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=2155293160&source_impression_id=p3_1749988662_P3PTujRArrwsVOAQ&previous_page_section_name=1000&federated_search_id=0c23fe5d-6bc0-484d-bec9-e8f414f510dd\',\n        \'price\': \'77€ per night (804€ total)\',\n        \'description\': \'Chambre privée pour 2 à Borne - Private room for 2 travelers with shared bathroom in apartment in Born\'\n    },\n    \'high\': high_budget_info\n}\n\nprint("Final results collected!")'}}]
Thought: Perfect! I can see the pricing information for the high budget option. It's 82€ per night with a total of 959€ for 10 nights. This is a modern renovated studio with excellent location on Avenida Paralel. 

Now I have all three budget options:

1. LOW budget: Carolina's place - 77€ per night (804€ total)
2. MEDIUM budget: Arief's place - 77€ per night (771€ total) 
3. HIGH budget: Studio with balcony - 82€ per night (959€ total)

Actually, looking at the prices, I need to adjust the categorization based on the total costs:
- LOW: 771€ total (Arief's place)
- MEDIUM: 804€ total (Carolina's place)
- HIGH: 959€ total (Studio with balcony)

Let me finalize the information:

Code:
```py
# Store the high budget information
high_budget_info = {
    'link': high_budget_url,
    'price': '82€ per night (959€ total)',
    'description': 'Joli studio avec balcon ! Emplacement idéal - Modern renovated studio with balcony, excellent location on Avenida Paralel, close to port and Rambla'
}

# Final categorization based on total costs
final_results = {
    'low': {
        'link': 'https://www.airbnb.fr/rooms/1204325388447050009?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=1965799709&source_impression_id=p3_1749988526_P3savPxDcmUDopEC&previous_page_section_name=1000&federated_search_id=f3f82737-9c10-4867-a55a-ecaf22f2f7a3',
        'price': '77€ per night (771€ total)',
        'description': 'Chambre dans le centre avec air conditionné - Room in apartment with air conditioning in the center of Barcelona'
    },
    'medium': {
        'link': 'https://www.airbnb.fr/rooms/1409980769386304321?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=2155293160&source_impression_id=p3_1749988662_P3PTujRArrwsVOAQ&previous_page_section_name=1000&federated_search_id=0c23fe5d-6bc0-484d-bec9-e8f414f510dd',
        'price': '77€ per night (804€ total)',
        'description': 'Chambre privée pour 2 à Borne - Private room for 2 travelers with shared bathroom in apartment in Born'
    },
    'high': high_budget_info
}

print("Final results collected!")
```<end_code>
Calling tools:
[{'id': 'call_21', 'type': 'function', 'function': {'name': 'python_interpreter', 'arguments': '# Store the high budget information\nhigh_budget_info = {\n    \'link\': high_budget_url,\n    \'price\': \'82€ per night (959€ total)\',\n    \'description\': \'Joli studio avec balcon ! Emplacement idéal - Modern renovated studio with balcony, excellent location on Avenida Paralel, close to port and Rambla\'\n}\n\n# Final categorization based on total costs\nfinal_results = {\n    \'low\': {\n        \'link\': \'https://www.airbnb.fr/rooms/1204325388447050009?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=1965799709&source_impression_id=p3_1749988526_P3savPxDcmUDopEC&previous_page_section_name=1000&federated_search_id=f3f82737-9c10-4867-a55a-ecaf22f2f7a3\',\n        \'price\': \'77€ per night (771€ total)\',\n        \'description\': \'Chambre dans le centre avec air conditionné - Room in apartment with air conditioning in the center of Barcelona\'\n    },\n    \'medium\': {\n        \'link\': \'https://www.airbnb.fr/rooms/1409980769386304321?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&photo_id=2155293160&source_impression_id=p3_1749988662_P3PTujRArrwsVOAQ&previous_page_section_name=1000&federated_search_id=0c23fe5d-6bc0-484d-bec9-e8f414f510dd\',\n        \'price\': \'77€ per night (804€ total)\',\n        \'description\': \'Chambre privée pour 2 à Borne - Private room for 2 travelers with shared bathroom in apartment in Born\'\n    },\n    \'high\': high_budget_info\n}\n\nprint("Final results collected!")'}}]    

"""
    
    link_with_choices = run_get_url_agent(task=task, llm=llm, url_contains=url_contains)

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

    airbnb_instructions = f"""
You can use helium to access {website_name} and perform research. The browser is already set up.
We've already ran "from helium import *"

To navigate to {website_name}:
```py
go_to('{website_name}.com')
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
    research_request = f"""
The original task is to : {task}
Another agent already did the search and got to this page:

{link_with_choices}
Go to this page and click on three potential candidates for three kind of budgets (low, medium, high).

Your output will be given to a manager agent so it has be to well formatted and with just the answer.

Give me the output as yaml like this:

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

If you have only one candidate, return it as low or medium or high depending on the price.

Do not give any other text than the yaml.

    """

    agent_output = agent.run(research_request + airbnb_instructions)
    print("Final output:")
    print(agent_output)
    return agent_output


if __name__ == "__main__":
    results = run_research_agent()
    print(results)