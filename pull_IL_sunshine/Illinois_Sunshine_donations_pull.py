"""
This file will be used to pull all donations linked to bill sponsors from the 
Illinois Sunshine database.
website: https://illinoissunshine.org/
"""
import csv
import httpx
import io
from lxml import html
import json
import re

def match_sponsor_to_candidate(name: str) -> list[str]:
    """
    First step: use the lookup URL, use the JSON file it returns to match
    names and get relevant ID candidate numbers.
    [[make a better doc string]]
    """
    name_split = name.split()
    first_name = name_split[0]
    last_name = name_split[1]
    if len(name_split) > 2:
        title = name_split[2]
    else:
        title = None

    url = "https://illinoissunshine.org/api/advanced-search/"

    headers = {
        "referer" : "https://illinoissunshine.org/search/?term=Sara+Feigenholtz&table_name=candidates&search_date__ge=&search_date__le="
    }

    params = {
        "term" : name,
        "table_name" : "candidates",
        "draw" : "1",
        "columns[0][data]" : "last_name",
        "columns[0][searchable]" : "true",
        "columns[0][orderable]" : "true",
        "columns[0][search][regex]" : "false",
        "columns[1][data]" : "party",
        "columns[1][searchable]" : "true",
        "columns[1][orderable]" : "true",
        "columns[1][search][regex]" : "false",
        "columns[2][data]" : "office",
        "columns[2][searchable]" : "true",
        "columns[2][orderable]" : "true",
        "columns[2][search][regex]" : "false",
        "order[0][column]" : "0",
        "order[0][dir]" : "asc",
        "start" : "0",
        "length" : "10",
        "search[regex]" : "false",
        "_" : "1770178172833"
    }

    id_list = []
    with httpx.Client(headers = headers) as c:
        response = c.get(url, params = params)
        json_dic = json.loads(response.text)
        for candidate in json_dic["objects"]["candidates"]:
            if (first_name in candidate["first_name"] and
                last_name in candidate["last_name"]):
                # Check on appropriate title or lack thereof
                if title is None:
                    if not (re.search(r'Jr|II+', first_name) or re.search(r'Jr|II+', last_name)):
                        id_list.append(candidate["id"])
                else:
                    if re.search(title, first_name) or re.search(title, last_name):
                        id_list.append(candidate["id"])
        return id_list


def get_committee_ids(candidate_ids: list[str]):
    """
    [[write a doc string]]
    """
    unique_committee_ids = set()
    for candidate_id in candidate_ids:
        response = httpx.get(f"https://illinoissunshine.org/candidates/{candidate_id}/")
        root = html.fromstring(response.text)
        
        table = root.cssselect("table.table.table-striped")[0]
        
        for link in table.cssselect("a"):
            committee_url = link.get("href")
            committee_id = committee_url.rstrip("/").split("-")[-1]
            unique_committee_ids.add(committee_id)
    
    committee_ids = list(unique_committee_ids)
    return committee_ids


def download_donations(committee: str):
    """
    [[write a doc string]]
    """
    response = httpx.get(f"https://illinoissunshine.org/api/receipts/?committee_id={committee}&datatype=csv&limit=100000", headers={"Referer": f"https://illinoissunshine.org/committees/{committee}/"})
    return csv.reader(io.StringIO(response.text))


if __name__ == "__main__":
    with open("pull_IL_sunshine/intermediate_data/unique_sponsors.csv", "r") as name_list:
        next(name_list)
        reader = csv.reader(name_list)
        for name in reader:
            sponsor = name[1]
            filepath = f"donations/{sponsor}.csv"

            ids = get_committee_ids(match_sponsor_to_candidate(sponsor))
            with open(filepath, "w") as f:
                writer = csv.writer(f)
                for id in ids:
                    writer.writerows(download_donations(id))
        