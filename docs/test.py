import argparse
from io import BytesIO
from time import sleep
import json
import re
from typing import List, Dict

import helium
from dotenv import load_dotenv
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from smolagents import CodeAgent, DuckDuckGoSearchTool, tool, LiteLLMModel
from smolagents.agents import ActionStep
from smolagents.cli import load_model
import os

# Configuration de l'API
os.environ["OPENAI_API_KEY"] = "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"

# Prompt principal pour l'agent de récupération de liens de vols
flight_links_request = """
I am a flight booking assistant. I need to analyze Google Flights search results and extract direct booking links for flights.

Your task is to:
1. Navigate to the provided Google Flights search URL
2. Wait for the page to load completely and show flight results
3. Find and extract the booking links for the first 5 flight options
4. For each flight, collect:
   - The airline name
   - Departure and arrival times
   - Price
   - Direct booking link (URL)
   - Flight duration
   - Number of stops (if any)

Please be methodical and wait for pages to load properly. Focus on finding clickable booking buttons or links that lead to airline booking pages.
"""

def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract flight booking links from Google Flights search results.")
    parser.add_argument(
        "flights_url",
        type=str,
        help="The Google Flights search URL to analyze"
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="LiteLLMModel",
        help="The model type to use"
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default="gpt-4o",
        help="The model ID to use"
    )
    parser.add_argument(
        "--max-flights",
        type=int,
        default=5,
        help="Maximum number of flights to extract (default: 5)"
    )
    return parser.parse_args()

def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    sleep(1.0)  # Laisser le temps aux animations JavaScript
    driver = helium.get_driver()
    current_step = memory_step.step_number
    if driver is not None:
        # Nettoyer les anciens screenshots pour optimiser la mémoire
        for previous_memory_step in agent.memory.steps:
            if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
                previous_memory_step.observations_images = None
        
        png_bytes = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png_bytes))
        print(f"📸 Screenshot capturé: {image.size} pixels")
        memory_step.observations_images = [image.copy()]

    # Mettre à jour les observations avec l'URL actuelle
    url_info = f"Current URL: {driver.current_url}"
    memory_step.observations = (
        url_info if memory_step.observations is None else memory_step.observations + "\n" + url_info
    )
    return

@tool
def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    """
    Recherche du texte sur la page actuelle via Ctrl + F et va au nième résultat.
    Args:
        text: Le texte à rechercher
        nth_result: Quelle occurrence choisir (défaut: 1)
    """
    elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    if nth_result > len(elements):
        raise Exception(f"Résultat n°{nth_result} non trouvé (seulement {len(elements)} résultats)")
    result = f"Trouvé {len(elements)} résultats pour '{text}'."
    elem = elements[nth_result - 1]
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    result += f"Focus sur l'élément {nth_result} de {len(elements)}"
    return result

@tool
def go_back() -> None:
    """Retourne à la page précédente."""
    driver.back()

@tool
def close_popups() -> str:
    """
    Ferme les modales ou pop-ups visibles sur la page.
    """
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    return "Pop-ups fermés"

@tool
def wait_for_page_load(seconds: int = 3) -> str:
    """
    Attend que la page se charge complètement.
    Args:
        seconds: Nombre de secondes à attendre
    """
    sleep(seconds)
    return f"Attente de {seconds} secondes terminée"

@tool
def extract_flight_info() -> str:
    """
    Extrait les informations des vols visibles sur la page Google Flights.
    Retourne un JSON avec les détails des vols.
    """
    try:
        # Rechercher les éléments de vol sur la page
        flight_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="flight-card"], .pIav2d, .yR1fYc')
        
        if not flight_elements:
            # Essayer d'autres sélecteurs possibles
            flight_elements = driver.find_elements(By.CSS_SELECTOR, '[role="listitem"], .JMc5Xc')
        
        flights_info = []
        
        for i, element in enumerate(flight_elements[:5]):  # Limiter aux 5 premiers
            try:
                # Extraire les informations de chaque vol
                flight_data = {
                    "flight_number": i + 1,
                    "element_text": element.text[:200] if element.text else "No text",
                    "clickable": element.is_enabled() and element.is_displayed()
                }
                flights_info.append(flight_data)
            except Exception as e:
                print(f"Erreur lors de l'extraction du vol {i+1}: {e}")
                continue
        
        return json.dumps(flights_info, indent=2)
    
    except Exception as e:
        return f"Erreur lors de l'extraction: {str(e)}"

@tool
def get_current_url() -> str:
    """Retourne l'URL actuelle du navigateur."""
    return driver.current_url

@tool
def click_flight_option(flight_number: int) -> str:
    """
    Clique sur une option de vol spécifique.
    Args:
        flight_number: Numéro du vol à cliquer (1-5)
    """
    try:
        flight_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="flight-card"], .pIav2d, .yR1fYc')
        
        if not flight_elements:
            flight_elements = driver.find_elements(By.CSS_SELECTOR, '[role="listitem"], .JMc5Xc')
        
        if flight_number <= len(flight_elements):
            element = flight_elements[flight_number - 1]
            driver.execute_script("arguments[0].click();", element)
            sleep(2)  # Attendre le chargement
            return f"Cliqué sur le vol {flight_number}"
        else:
            return f"Vol {flight_number} non trouvé (seulement {len(flight_elements)} vols disponibles)"
    
    except Exception as e:
        return f"Erreur lors du clic sur le vol {flight_number}: {str(e)}"

def initialize_driver():
    """Initialise le WebDriver Selenium."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--window-size=1400,1000")
    chrome_options.add_argument("--disable-pdf-viewer")
    chrome_options.add_argument("--window-position=0,0")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return helium.start_chrome(headless=False, options=chrome_options)

def initialize_agent(model):
    """Initialise le CodeAgent avec le modèle spécifié."""
    return CodeAgent(
        tools=[
            DuckDuckGoSearchTool(), 
            go_back, 
            close_popups, 
            search_item_ctrl_f,
            wait_for_page_load,
            extract_flight_info,
            get_current_url,
            click_flight_option
        ],
        model=model,
        additional_authorized_imports=["helium", "time", "json", "re"],
        step_callbacks=[save_screenshot],
        max_steps=25,
        verbosity_level=2,
    )

# Instructions spécifiques pour helium et Google Flights
helium_instructions = """
Use helium to navigate websites and interact with Google Flights.
We've already imported helium: "from helium import *"

Key helium commands:
- go_to('url'): Navigate to a URL
- click("text"): Click on text or button
- click(Link("text")): Click on a link
- scroll_down(num_pixels=800): Scroll down
- scroll_up(num_pixels=800): Scroll up
- wait_until(lambda: Text('text').exists()): Wait for element

For Google Flights specifically:
1. First go to the provided Google Flights URL
2. Wait for the page to load completely (use wait_for_page_load(5))
3. Close any popups or cookie banners with close_popups()
4. Look for flight results and extract information
5. Try to click on flight options to get booking links
6. Be patient - Google Flights loads dynamically

Always take screenshots after each action to see the current state.
When you find booking buttons or "Select" buttons, click them to get airline booking links.

Important: Google Flights often has multiple steps:
1. Search results page
2. Flight details page after clicking a flight
3. Booking page or redirect to airline website

Your goal is to collect 5 flight booking links with their details.

Use your tools:
- extract_flight_info(): To get flight information from the current page
- click_flight_option(number): To click on a specific flight
- wait_for_page_load(seconds): To wait for page loading

Code example:
```py
go_to('https://www.google.com/travel/flights/...')
wait_for_page_load(5)
close_popups()
extract_flight_info()
```

At the end, provide a final answer with the collected flight information and booking links.
"""

def main():
    # Charger les variables d'environnement
    load_dotenv()

    # Parser les arguments de ligne de commande
    args = parse_arguments()

    # Initialiser le modèle
    model = LiteLLMModel(
        model_id='ollama_chat/qwen2:7b',
        api_base='http://127.0.0.1:11434',
        flatten_messages_as_text=False
    )

    global driver
    driver = initialize_driver()
    agent = initialize_agent(model)

    # Exécuter l'agent avec le prompt
    agent.python_executor("from helium import *")
    
    # Construire le prompt complet
    full_prompt = f"""
    {flight_links_request}
    
    Google Flights URL to analyze: {args.flights_url}
    
    Extract information and booking links for up to {args.max_flights} flights.
    
    {helium_instructions}
    """
    
    print(f"🛫 Démarrage de l'analyse des vols...")
    print(f"🔗 URL: {args.flights_url}")
    print(f"📊 Nombre de vols à extraire: {args.max_flights}")
    print("=" * 80)
    
    try:
        result = agent.run(full_prompt)
        print("=" * 80)
        print("✅ Analyse terminée!")
        print(f"📄 Résultat: {result}")
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {str(e)}")
    finally:
        # Fermer le navigateur
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()