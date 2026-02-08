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
    vars = ["Name", "Total_all", "Total_L3"] # Fill this in with var names
    writer = csv.DictWriter(file, fieldnames = vars)
    writer.writeheader()

    # Loop through each sponsor in the folder
    directory = 'donations'
    for filename in os.listdir(directory):
        filename = "Win Stoller.csv" ## I have this in here cause pandas is mad about the empty CSV files, feel free to remove if you solve this

        # Read in CSV for a sponsor and clean necessary vars
        df = pd.read_csv(f'donations/{filename}')
        df["received_date"] = pd.to_datetime(df["received_date"])
        df["last_3_years"] = df["received_date"] >= '01/01/2023'

        # Step 2: calculate stats
        row = {}
        row["Name"] = filename.replace(".csv", "")
        row["Total_all"] = df["amount"].sum()
        row["Total_L3"] = df["amount"][df["last_3_years"]].sum()

        # Step 3: write to a row of the CSV
        writer.writerow(row)