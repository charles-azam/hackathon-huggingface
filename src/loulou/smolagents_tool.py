from loulou.price_research_agent import find_three_candidates_on_website
from loulou.browser_use_tools import run_get_url_agent
from langchain_anthropic import ChatAnthropic
from smolagents import tool


@tool
def research_airbnb(task: str,) -> str:
    """
    Find three candidates on Airbnb for a given task.
    
    This tool will output a yaml with the three candidates.
    
    Here is an example of an input and output:
    
    input: 'search for a 2 bedroom apartment in the center of Barcelona for 2 people for 10 nights from 16/06/2025.'

    output:
'''
- low:
    - link: https://www.airbnb.fr/rooms/1426696850530973315?adults=2&check_in=2025-06-19&check_out=2025-06-28&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&children=0&infants=0&pets=0&photo_id=2183400057&source_impression_id=p3_1749990446_P3W6bU3PbD5pcYC8&previous_page_section_name=1000&federated_search_id=cd9b51e4-59fe-47ef-8610-68f17a502370
    - price: 94€ per night (873€ total)
    - description: Petite chambre privée près de la cathédrale - Private room for 2 people with individual lock and key for comfort, located in a shared apartment in the Gothic quarter near Barcelona cathedral
- medium:
    - link: https://www.airbnb.fr/rooms/1177998676371545286?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&source_impression_id=p3_1749990558_P35L4tWmLW_rLQsm&previous_page_section_name=1000&federated_search_id=505d111a-74a6-49ca-8ec6-953a02b2a3b4
    - price: 84€ per night (1044€ total)
    - description: Centre de 6 mètres de l'Español Stadium - Comfortable renovated apartment 20 min by metro from center, 5 min from Arco del Triunfo metro station. Located in Cornellà district with restaurants, bakeries, bars. 1 double bedroom and 2 singles, equipped kitchen, living room, bathroom with shower, air conditioning, wifi, Smart TV
- high:
    - link: https://www.airbnb.fr/rooms/11372386?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&source_impression_id=p3_1749990589_P3jRdmySjVJUfRSM&previous_page_section_name=1000&federated_search_id=6c568e77-574c-4dd4-bf71-eb18fc40fc11
    - price: 161€ per night (1912€ total)
    - description: Appart. Barcelone-Congrès - Modern apartment in a building next to Fira Barcelona and GranVia2 commercial center with great choice of leisure activities. Well connected to airport, 2 metro lines, bus, train and taxi. Located on Plaza Europa with stunning city views and modern amenities
'''
    
    
    Args:
        task (str, optional): The task to research on Airbnb.

    """
    llm: ChatAnthropic = ChatAnthropic(model="claude-sonnet-4-20250514")
    return find_three_candidates_on_website(task="GO to airbnb, " + task, website_name="airbnb", url_contains="homes", llm=llm)

@tool
def research_google_travel(task: str = "airbnb_research", llm: ChatAnthropic = ChatAnthropic(model="claude-sonnet-4-20250514")) -> str:
    """
    Find three candidates on Google Flights for a given task.
    
    This tool will output a yaml with the three candidates.
    
    Here is an example of an input and output:
    
    input: 'search for a flight from paris to barcelona 16/06/2025 to 26/06/2025.'

    output:
'''
- low:
    - link: https://www.airbnb.fr/rooms/1426696850530973315?adults=2&check_in=2025-06-19&check_out=2025-06-28&guests=2&search_mode=regular_search&category_tag=Tag%3A8678&children=0&infants=0&pets=0&photo_id=2183400057&source_impression_id=p3_1749990446_P3W6bU3PbD5pcYC8&previous_page_section_name=1000&federated_search_id=cd9b51e4-59fe-47ef-8610-68f17a502370
    - price: 94€ per night (873€ total)
    - description: Petite chambre privée près de la cathédrale - Private room for 2 people with individual lock and key for comfort, located in a shared apartment in the Gothic quarter near Barcelona cathedral
- medium:
    - link: https://www.airbnb.fr/rooms/1177998676371545286?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&source_impression_id=p3_1749990558_P35L4tWmLW_rLQsm&previous_page_section_name=1000&federated_search_id=505d111a-74a6-49ca-8ec6-953a02b2a3b4
    - price: 84€ per night (1044€ total)
    - description: Centre de 6 mètres de l'Español Stadium - Comfortable renovated apartment 20 min by metro from center, 5 min from Arco del Triunfo metro station. Located in Cornellà district with restaurants, bakeries, bars. 1 double bedroom and 2 singles, equipped kitchen, living room, bathroom with shower, air conditioning, wifi, Smart TV
- high:
    - link: https://www.airbnb.fr/rooms/11372386?adults=2&check_in=2025-06-16&check_out=2025-06-26&guests=2&search_mode=regular_search&source_impression_id=p3_1749990589_P3jRdmySjVJUfRSM&previous_page_section_name=1000&federated_search_id=6c568e77-574c-4dd4-bf71-eb18fc40fc11
    - price: 161€ per night (1912€ total)
    - description: Appart. Barcelone-Congrès - Modern apartment in a building next to Fira Barcelona and GranVia2 commercial center with great choice of leisure activities. Well connected to airport, 2 metro lines, bus, train and taxi. Located on Plaza Europa with stunning city views and modern amenities
'''
    
    
    Args:
        task (str, optional): The task to research on Google Flights.

    """
    return find_three_candidates_on_website(task="GO to https://www.google.com/travel/flights, " + task, website_name="www.google.com/travel/flights", url_contains="search")