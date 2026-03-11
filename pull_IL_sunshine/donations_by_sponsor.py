"""
This file takes in CSVs with donation information by sponsor and outputs a
a table that links sponser name to a variety of statistics about their donations
"""

import pandas as pd
import os
import csv

COLS = [
    "name",
    "donation_count_all",
    "donation_count_L3",
    "total_all",
    "total_L3",
    "pct_c_above_all",
    "pct_c_above_L3",
    "avg_donation_all",
    "avg_donation_L3",
    "amt_allcond_all",
    "amt_allcond_L3",
    "pct_c_allcond_all",
    "pct_c_allcond_L3",
    "pct_c_IL_all",
    "pct_c_IL_L3",
    "first_donation_year",
]

ENTITY_KEYWORDS = r"PAC|INC|LLC|Corp|Committee|Assoc|Union"
LAST_3_YR_CUTOFF = "01/01/2023"

# Threshold that requires expedited schedule 1A reporting
LARGE_DONATION = 1000


def get_unique_sponsor_filenames() -> list[str]:
    """
    Create a list of filenames containing each individual sponsor's donations,
    with filenames in "<sponsorname>.csv" format.

    Inputs: None

    Outputs:
        A list of strings, with each string containing a unique filename.
    """

    filenames = []

    with open("pull_IL_sunshine/intermediate_data/unique_sponsors.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            filenames.append(row["Sponsor"] + ".csv")

    return filenames


def remove_null_donations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop donations with no recorded value or date recieved.

    Inputs:
        df (pd.DataFrame): A dataframe with all of a sponsor's donations

    Outputs:
        A filtered pd.DataFrame
    """

    df["received_date"] = pd.to_datetime(df["received_date"], errors="coerce")
    df = df.dropna(subset=["received_date"])

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    return df

def safe_divide(numerator, denominator):
    """
    Return numerator / denominator or fill_value if denominator is 0.
    """
    if denominator > 0:
        return numerator / denominator 
    else:
        return pd.NA

def calculate_summary_stats(
    df: pd.DataFrame, name: str
) -> dict[str, str | float | int]:
    """
    Calculate a full set of summary stats on each sponsor's donations.

    Input:
        df (pd.DataFrame): A filtered dataframe with a sponsor's donations

    Outputs:
        A dictionary of summary stats to be added to the final output CSV
    """
    row = {}

    # Pre-calculate mask and lengths
    df["last_3_years"] = df["received_date"] >= LAST_3_YR_CUTOFF
    total_len = len(df)
    L3_len = df["last_3_years"].sum()

    # Name
    row["name"] = name

    # Donation counts and totals
    row["donation_count_all"] = total_len
    row["donation_count_L3"] = L3_len
    row["total_all"] = df["amount"].sum()
    row["total_L3"] = df.loc[df["last_3_years"], "amount"].sum()

    # Large donations
    row["pct_c_above_all"] = safe_divide((df["amount"] > LARGE_DONATION).sum(), total_len)   
    row["pct_c_above_L3"] = safe_divide((
        df["last_3_years"] & (df["amount"] > LARGE_DONATION)
    ).sum(), L3_len)

    # Average donation sizes
    row["avg_donation_all"] = df["amount"].mean()
    row["avg_donation_L3"] = df.loc[df["last_3_years"], "amount"].mean()

    # Donations from entities
    entity_mask = (
        (df["d2_part"] != "1A")
        & (df["first_name"].isna())
        & (df["last_name"].str.contains(ENTITY_KEYWORDS, case=False))
    )

    # Entity vs Individual
    row["amt_allcond_all"] = df.loc[entity_mask, "amount"].sum()
    row["amt_allcond_L3"] = df.loc[entity_mask & df["last_3_years"], "amount"].sum()
    
    row["pct_c_allcond_all"] = safe_divide(entity_mask.sum(), total_len)
    row["pct_c_allcond_L3"] = safe_divide((entity_mask & df["last_3_years"]).sum(), L3_len)

    # In-state (Illinois) vs. out-of-state donations
    row["pct_c_IL_all"] = safe_divide((df["state"] == "IL").sum(), total_len)
    row["pct_c_IL_L3"] = safe_divide((df["last_3_years"] & (df["state"] == "IL")).sum(), L3_len)

    # 16. first_donation_year
    row["first_donation_year"] = int(pd.to_datetime(df["received_date"]).min().year)

    return row


def main():
    # Set up csv output file
    with open("pull_IL_sunshine/intermediate_data/donation_stats.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=COLS, restval="")
        writer.writeheader()

        # Loop through each sponsor in the folder
        filenames = get_unique_sponsor_filenames()

        for filename in filenames:
            path = os.path.join("donations", filename)
            name = filename.replace(".csv", "")
            # Read in CSV for each sponsor
            try:
                df = pd.read_csv(path)
            # Write empty rows for sponsors without a matching file
            except FileNotFoundError:
                row = {}
                row["name"] = name
                writer.writerow(row)
                continue

            df = remove_null_donations(df)
            row = calculate_summary_stats(df, name)
            writer.writerow(row)


if __name__ == "__main__":
    main()
