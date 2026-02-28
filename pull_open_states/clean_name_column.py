"""
This file reads in the cleaned Open States data, adds a column with cleaned
names and outputs the finalized Open States dataset.
"""

import pandas as pd
import re
from unidecode import unidecode
from pathlib import Path

def general_cleaning(name):
    """
    Step 0: Cleaning
    We want to do some basic cleaning before attempting to match. The goal is 
    to have clean names in the following format: First Last + Jr/II/III

    - First names should always be the first string of text. Last names should
        be either the last word or the last word before the comma or “and.”
    - Remove all punctuation and accent marks. This includes extra spaces between
        words.
    - ID the title, likely just by checking if the string contains Jr, II, or III.
    
    For example, after cleaning “Edgar González and   Jr.” would become 
    “Edgar Gonzalez Jr” in the clean names column.
    """
    name = unidecode(name)
    first = re.findall(r'\A\w+\b', name)[0]
    last = re.findall(r'\b(\w+)\b(?=\s*(?:,|\band\b|$))',name)[0]
    title_list = re.findall(r'I+|Jr', name)

    if title_list != []:
        title = title_list[0]
        return " ".join([first, last, title])
    else:
        return " ".join([first, last])

# Fix specific instances of nicknames or name changes
def specific_changes(clean_name):
    names_to_change = {"Michael Coffey Jr" : "Mike Coffey",
                    "Sandra Hamilton" : "Sandy Hamilton",
                    "William Hauter" : "Bill Hauter",
                    "Suzy Hilton" : "Suzanne Hilton",
                    "Anne Murray" : "Anne Stava",
                    "Dave Vella" : "David Vella",
                    "Frances Hurley" : "Fran Hurley",
                    "Michael Marron" : "Mike Marron",
                    "Daniel Swanson" : "Dan Swanson",
                    "Napoleon Harris III" : "Napoleon Harris",
                    "Kimberly Buclet" : "Kim DuBuclet",
                    "Angelica Cuellar" : "Angie Cuellar",
                    "Thomas Morrison" : "Tom Morrison",
                    "Lamont Robinson Jr" : "Lamont Robinson"}
    if clean_name in names_to_change.keys():
        return names_to_change[clean_name]
    else:
        return clean_name

# Apply function to all rows of the primary_sponsor_1 column
openstates = pd.read_csv("pull_open_states/intermediate_data/openstates_cleaned.csv")
openstates["primary_sponsor_1_clean"] = openstates["primary_sponsor_1"].apply(general_cleaning)
openstates["primary_sponsor_1_clean"] = openstates["primary_sponsor_1_clean"].apply(specific_changes)
openstates.drop(openstates.columns[0], axis = 1, inplace=True)

# Output full dataset
openstates.to_csv("pull_open_states/intermediate_data/openstates_w_names.csv")

# Create a list of unique primary sponsors
unique_sponsors = pd.DataFrame(openstates["primary_sponsor_1_clean"].unique(),
                               columns=["Sponsor"])

unique_sponsors_out_path = Path("pull_IL_sunshine/intermediate_data/unique_sponsors.csv")
unique_sponsors_out_path.parent.mkdir(parents=True, exist_ok=True)

unique_sponsors.to_csv("pull_IL_sunshine/intermediate_data/unique_sponsors.csv")

# Output final, trimmed dataset
columns_to_keep = ["identifier", "session_identifier", "organization_classification",
                   "first_action", "primary_sponsor_1", "num_sponsors",
                   "became_law", "first_committee_referral_date", "committee_passages",
                   "passed_first_chamber", "passed_full_legislature"]

final_out_path = Path("final_data/bills.csv")
final_out_path.parent.mkdir(parents=True, exist_ok=True)
openstates[columns_to_keep].to_csv("final_data/bills.csv")
