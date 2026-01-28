import httpx
import json
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import exploration.endpoint_params as params

def get_api_ref():
    try:
        filepath = Path(__file__).parent / "api_ref.json"
        with open(filepath, "r") as file:
            api_ref = json.load(file)
        return api_ref
    except FileNotFoundError:
        print("Error Opening API Reference File: Not Found")
  
API_KEY = os.getenv("OPEN_STATES_API_KEY")
API_REF = get_api_ref()

def main():
    print("Hello from project-il-legible!")
    bills = get_bills()
    people = get_people()

    print(bills)

    
def construct_endpoint_url(endpoint, id=None, params=None):
    url = httpx.URL(f"{API_REF["base_url"]}{endpoint}/{id if id is not None else ''}?apikey={API_KEY}")

    if(params):
        params = dict(url.params) | params
        url = url.copy_with(params=params)

    return str(url)
    

def get_bills(max_pages=100):
    
    bills = []
    page = 1

    for i in range(1, max_pages+1):
        q_params = params.BILLS | {"page": i}
        url = construct_endpoint_url("/bills", params=(params.BILLS | {"page": page}))
        data = make_request(url)
        bills.extend(data["results"])

        pg = data["pagination"]

        if(pg["page"] == max_pages or pg["page"] == pg["max_page"]):
            break

        page = pg["page"] + 1
        
    return bills

def get_people(person_id=None, max_pages=1):
    url = construct_endpoint_url("/people", id=person_id, params=params.PEOPLE)
    return make_request(url)



def get_params_keys(endpoint):
    """
    Get a list of param keys for a given endpoint
    
    :param endpoint: The endpoint for which to get params
    """
    params = API_REF["endpoints"][endpoint]["search"]["query_parameters"]
    return params.keys()



def make_request(url):
    try:
        time.sleep(6)
        resp = httpx.get(url, follow_redirects=True)
        return resp.json()
    except:
        print("Error making request to ", url)



if __name__ == "__main__":
    load_dotenv()
    main()
