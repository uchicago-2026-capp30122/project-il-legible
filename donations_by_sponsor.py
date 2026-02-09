"""
This file takes in CSVs with donation information by sponsor and outputs a
a table that links sponser name to a variety of statistics about their donations

TO BE DELETED LATER
List of the stats we want:
** All of these to be calculated for all time and the last 3(?) years **
- Total donations
- Percent donations above a certain amount (100k?)
- Average donation amount
- Amount donations non 1A entities (corporations)
- Percent donations non 1A entities (corporations)
- Amount donations from no first name (corporations)
- Percent donations from no first name (corporations)
- Amount donations from LLC corps (corporations)
- Percent donations from LLC corps (corporations)
- Amount donations in state (vs out of state)
- Percent donations in state (vs out of state)
- First donation
- Last donation
"""
import pandas as pd
import os
import csv

#Set up csv output file
with open("donation_stats.csv", "w") as file:
    vars = [
    "Name",
    "Total_all", "Total_L3",
    "pct_above_all", "pct_above_L3",
    "avg_donation_all", "avg_donation_L3",
    "amt_non1a_all", "amt_non1a_L3",
    "pct_non1a_all", "pct_non1a_L3",
    "amt_nofirst_all", "amt_nofirst_L3",
    "pct_nofirst_all", "pct_nofirst_L3",
    "amt_LLC_all", "amt_LLC_L3",
    "pct_LLC_all", "pct_LLC_L3",
    "amt_IL_all", "amt_IL_L3",
    "pct_IL_all", "pct_IL_L3",
    "yrs_since_first", "yrs_since_last",
]
    writer = csv.DictWriter(file, fieldnames = vars)
    writer.writeheader()

    # Loop through each sponsor in the folder
    total_names = 0
    working_names = 0

    directory = 'donations'
    for filename in os.listdir(directory):
        total_names += 1

        path = os.path.join(directory, filename)

        # Read in CSV for a sponsor and clean necessary vars
        try:
            df = pd.read_csv(path)
            working_names += 1
        except pd.errors.EmptyDataError:
            continue

        df["received_date"] = pd.to_datetime(df["received_date"], errors="coerce")
        df = df.dropna(subset=["received_date"])
        
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["amount"])
        
        df["last_3_years"] = df["received_date"] >= '01/01/2023'

        # Step 2: calculate stats
        total_len = len(df)
        L3_len = df["last_3_years"].sum()

        row = {}
        row["Name"] = filename.replace(".csv", "")
        
        row["Total_all"] = df["amount"].sum()
        row["Total_L3"] = df.loc[df["last_3_years"], "amount"].sum()

        row["pct_above_all"] = (df["amount"] > 5000).sum() / total_len
        row["pct_above_L3"] = (df["last_3_years"] & (df["amount"] > 5000)).sum() / L3_len

        row["avg_donation_all"] = df["amount"].mean()
        row["avg_donation_L3"] = df.loc[df["last_3_years"], "amount"].mean()

        row["amt_non1a_all"] = df.loc[(df["d2_part"] != "1A"), "amount"].sum()
        row["amt_non1a_L3"] = df.loc[((df["d2_part"] != "1A") & df["last_3_years"]) , "amount"].sum()

        row["pct_non1a_all"] = (df["d2_part"] != "1A").sum() / total_len
        row["pct_non1a_L3"] = (df["last_3_years"] & (df["d2_part"] != "1A")).sum() / L3_len

        row["amt_nofirst_all"] = df.loc[df["first_name"].isna(), "amount"].sum()
        row["amt_nofirst_L3"] = df.loc[(df["first_name"].isna() & df["last_3_years"]) , "amount"].sum()

        row["pct_nofirst_all"] = df["first_name"].isna().sum() / total_len
        row["pct_nofirst_L3"] = (df["last_3_years"] & df["first_name"].isna()).sum() / L3_len

        row["amt_LLC_all"] = df.loc[(df["last_name"].str.contains("LLC")), "amount"].sum()
        row["amt_LLC_L3"] = df.loc[(df["last_name"].str.contains("LLC") & df["last_3_years"]) , "amount"].sum()

        row["pct_LLC_all"] = df["last_name"].str.contains("LLC").sum() / total_len
        row["pct_LLC_L3"] = (df["last_3_years"] & df["last_name"].str.contains("LLC")).sum() / L3_len

        row["amt_IL_all"] = df.loc[(df["state"] == "IL"), "amount"].sum()
        row["amt_IL_L3"] = df.loc[((df["state"] == "IL") & df["last_3_years"]) , "amount"].sum()

        row["pct_IL_all"] = (df["state"] == "IL").sum() / total_len
        row["pct_IL_L3"] = (df["last_3_years"] & (df["state"] == "IL")).sum() / L3_len

        row["yrs_since_first"] = pd.Timestamp.today().year - pd.to_datetime(df["received_date"]).min().year

        row["yrs_since_last"] = pd.Timestamp.today().year - pd.to_datetime(df["received_date"]).max().year

        # Step 3: write to a row of the CSV
        writer.writerow(row)
    print("working names: ", working_names)
    print("working name percentage: ", (working_names / total_names)*100)