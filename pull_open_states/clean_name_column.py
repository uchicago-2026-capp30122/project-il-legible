"""
This file reads in the cleaned Open States data, adds a column with cleaned
names and outputs the finalized Open States dataset.
"""

import pandas as pd
import re
from unidecode import unidecode

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

# Apply function to all rows of the primary_sponsor_1 column
openstates = pd.read_csv("openstates_cleaned.csv")
openstates["primary_sponsor_1_clean"] = openstates["primary_sponsor_1"].apply(general_cleaning)
openstates.drop(openstates.columns[0], axis = 1, inplace=True)

# Fix specific instances
# Angelica Cuellar -> Angie Cuellar

# Output final dataset
openstates.to_csv("openstates_w_names.csv")

# Create a list of unique primary sponsors
unique_sponsors = pd.DataFrame(openstates["primary_sponsor_1_clean"].unique(),
                               columns=["Sponsor"])
unique_sponsors.to_csv("../pull_IL_sunshine/unique_sponsors.csv")
