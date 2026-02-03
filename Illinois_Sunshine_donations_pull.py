"""
This file will be used to pull all donations linked to bill sponsors from the 
Illinois Sunshine database.
website: https://illinoissunshine.org/
"""
import csv
import httpx
import io

def match_sponsor_to_committee(name: str):
    ## First step: use the lookup URL, use the JSON file it returns to match
    ## names and get relevant ID candidate numbers [Elie]

    ## Second step: go to candidate pages using ID numbers [Max]
    ## (https://illinoissunshine.org/candidates/7821/) and pull committee ID numbers

def download_donations(committees: list):
    """
    [[write a doc string]]
    """
    for committee in committees:
        response = httpx.get(f"https://illinoissunshine.org/api/receipts/?committee_id={committee}&datatype=csv&limit=100000", headers={"Referer": f"https://illinoissunshine.org/committees/{committee}/"})

        data = csv.reader(io.StringIO(response.text))

        with open("test", "w") as f:
            writer = csv.writer(f)
            writer.writerows(data)
