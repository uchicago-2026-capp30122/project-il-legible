"""
This file reads in the cleaned Open States data, adds a column with cleaned
names and outputs the finalized Open States dataset.
"""

import pandas as pd
import re
from unidecode import unidecode
from pathlib import Path

def general_name_cleaning(name: str) -> str:
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

    Inputs:
        Name (str): An uncleaned name
    
    Outputs:
        A cleaned name
    """
    # Skip entries with blank sponsor names
    if not name:
        return ""

    name = unidecode(name)
    first = re.findall(r'\A\w+\b', name)[0]
    last = re.findall(r'\b(\w+)\b(?=\s*(?:,|\band\b|$))', name)[0]
    title_list = re.findall(r'I+|Jr', name)

    if title_list != []:
        title = title_list[0]
        return " ".join([first, last, title])
    else:
        return " ".join([first, last])


def specific_name_changes(clean_name: str) -> str:
    """
    Fix specific instances of nicknames or name changes that are not captured
    by the general cleaning algorithim.

    Inputs: 
        clean_name (str): A name returned by the initial cleaning steps
    
    Outputs:
        A cleaned name based on final manual adjustments
    """
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


def clean_sponsor_names(bills: pd.DataFrame) -> pd.DataFrame:
    """
    Apply sponsor name cleaning rules to both Sponsor Names column in the

    Inputs:
        bills_cleaned (pd.DataFrame): A dataframe with summarized bill information
        and cleaned sponsor names.
    
    Outputs:
        None. Directly saves a CSV
    """
    sponsor_cols = ["primary_sponsor_1", "primary_sponsor_2"]
    for col in sponsor_cols:
        bills[f"{col}_clean"] = bills[f"{col}"].fillna("").apply(general_name_cleaning).apply(specific_name_changes)
        #bills[f"{col}_clean"] = bills[f"{col}_clean"]
    bills.drop(bills.columns[0], axis = 1, inplace=True)

    return bills


def output_unique_sponsors_csv(bills_cleaned: pd.DataFrame) -> None:
    """
    Generates and saves a CSV with all unique primary bill sponsors to use in
    the Illinois Sunshine campaign donation data pipeline.

    Inputs:
        bills_cleaned (pd.DataFrame): A dataframe with summarized bill information
        and cleaned sponsor names.
    
    Outputs:
        None. Directly saves a CSV
    """
    unique_sponsors = pd.DataFrame(bills_cleaned["primary_sponsor_1_clean"].unique(),
                                columns=["Sponsor"])

    unique_sponsors_out_path = Path("pull_IL_sunshine/intermediate_data/unique_sponsors.csv")
    unique_sponsors_out_path.parent.mkdir(parents=True, exist_ok=True)

    unique_sponsors.to_csv("pull_IL_sunshine/intermediate_data/unique_sponsors_test.csv")
    return None


def output_final_bills_csv(bills_cleaned: pd.DataFrame) -> None:
    """
    Generates and saves a consolidated CSV with all key and cleaned bill data.

    Inputs:
        bills_cleaned (pd.DataFrame): A dataframe with summarized bill information
        and cleaned sponsor names.
    
    Outputs:
        None. Directly saves a CSV
    """
    cols_final = ["identifier", "session_identifier", "organization_classification",
                "first_action", "primary_sponsor_1_clean", "primary_sponsor_2_clean", 
                "num_sponsors", "became_law", "referred_to_committee", "committee_passages",
                "passed_first_chamber", "passed_full_legislature"]

    filepath = Path("final_data/bills_test.csv")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    bills_cleaned[cols_final].to_csv(filepath)

    return None


def main():
    bills = pd.read_csv("pull_open_states/intermediate_data/openstates_cleaned.csv")
    bills_cleaned = clean_sponsor_names(bills)

    # Save CSV with full dataset before tirmming down to final versions
    bills_cleaned.to_csv("pull_open_states/intermediate_data/openstates_w_names_test.csv")

    output_unique_sponsors_csv(bills_cleaned)
    output_final_bills_csv(bills_cleaned)

if __name__ == "__main__":
    main()