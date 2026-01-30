import httpx
import json
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

def main():
    print("Hello from project-il-legible!")
    bills = get_bills()

    print(bills)

    

def get_bills():
    return get_data_from_csv("bills")

# def get_people(person_id=None, max_pages=1):
#     return get_data_from_csv(url)

def get_sponsors():
    return get_data_from_csv("sponsorships")

def get_data_from_csv(file_fragment):
    root_dir = Path(os.getcwd())
    file_list = list(root_dir.rglob(f"./*/bulk_data/IL/*/*{file_fragment}.csv")) 
    df = None
    df = pd.concat((pd.read_csv(f) for f in file_list), ignore_index=True)
    
    return df


if __name__ == "__main__":
    load_dotenv()
    main()
