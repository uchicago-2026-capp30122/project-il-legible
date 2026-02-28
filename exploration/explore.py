import httpx
import json
import os
import time
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

INCLUDED_DATA = {
    "bill_abstracts",
    "actions",
    "bill_sponsorships",
    "bills",
    "organizations",
    "vote_counts",
    "votes",
    "vote_people"
}

def main():
    print("Hello from project-il-legible!")
    bills = get_bills()

    print(bills)

    
def get_all_datasets():
    datasets = dict.fromkeys(INCLUDED_DATA)
    for set in datasets:
        datasets[set] = get_data_from_csv(set)

    return datasets

def get_bills():
    return get_data_from_csv("bills")

def get_votes():
    return get_data_from_csv("votes")

def get_sponsors():
    return get_data_from_csv("sponsorships")

def get_data_from_csv(file_fragment):
    root_dir = Path(__file__).parent
    file_list = list(root_dir.rglob(f"bulk_data/IL/*/*{file_fragment}.csv")) 
    df = None
    df = pd.concat((pd.read_csv(f) for f in file_list), ignore_index=True)
    
    return df


if __name__ == "__main__":
    load_dotenv()
    main()
