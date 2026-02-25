"""
This file takes in CSVs with donation information by sponsor and outputs a
a table that links sponser name to a variety of statistics about their donations

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
with open("pull_IL_sunshine/intermediate_data/donation_stats.csv", "w") as file:
    vars = [
    "Name",
    "donation_count_all", "donation_count_L3",
    "total_all", "total_L3",
    "pct_c_above_all", "pct_c_above_L3",
    "pct_$_above_all", "pct_$_above_L3",
    "avg_donation_all", "avg_donation_L3",
    "amt_non1a_all", "amt_non1a_L3",
    "pct_c_non1a_all", "pct_c_non1a_L3",
    "pct_$_non1a_all", "pct_$_non1a_L3",
    "amt_nofirst_all", "amt_nofirst_L3",
    "pct_c_nofirst_all", "pct_c_nofirst_L3",
    "pct_$_nofirst_all", "pct_$_nofirst_L3",
    "amt_entity_all", "amt_entity_L3",
    "pct_c_entity_all", "pct_c_entity_L3",
    "pct_$_entity_all", "pct_$_entity_L3",
    "amt_allcond_all", "amt_allcond_L3",
    "pct_c_allcond_all", "pct_c_allcond_L3",
    "pct_$_allcond_all", "pct_$_allcond_L3",
    "amt_IL_all", "amt_IL_L3",
    "pct_c_IL_all", "pct_c_IL_L3",
    "pct_$_IL_all", "pct_$_IL_L3",
    "yrs_since_first", "yrs_since_last",
]
    writer = csv.DictWriter(file, fieldnames = vars, restval='')
    writer.writeheader()

    # Loop through each sponsor in the folder
    total_names = 0
    working_names = 0

    directory = 'donations'
    with open("pull_IL_sunshine/intermediate_data/unique_sponsors.csv", "r") as file:
        reader = csv.DictReader(file)
        unique_names = []
        for row in reader:
            unique_names.append(row["Sponsor"] + ".csv")
    for filename in unique_names:
        total_names += 1

        path = os.path.join(directory, filename)

        # Read in CSV for a sponsor and clean necessary vars
        try:
            df = pd.read_csv(path)
            working_names += 1
        except FileNotFoundError:
            row = {}
            row["Name"] = filename.replace(".csv", "")
            writer.writerow(row)
            continue

        df["received_date"] = pd.to_datetime(df["received_date"], errors="coerce")
        df = df.dropna(subset=["received_date"])
        
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["amount"])
        
        df["last_3_years"] = df["received_date"] >= '01/01/2023'

        # Step 2: calculate stats
        keywords = r"PAC|INC|LLC|Corp|Committee|Assoc|Union"
        # This is the amount significant enough to require expedited schedule 1A reporting
        large_donation = 1000

        row = {}
        row["Name"] = filename.replace(".csv", "")
        
        total_len = len(df)
        L3_len = df["last_3_years"].sum()
        row["donation_count_all"] = total_len
        row["donation_count_L3"] = L3_len

        total_all = df["amount"].sum()
        row["total_all"] = total_all
        total_L3 = df.loc[df["last_3_years"], "amount"].sum()
        row["total_L3"] = total_L3

        row["pct_c_above_all"] = (df["amount"] > large_donation).sum() / total_len
        row["pct_c_above_L3"] = (df["last_3_years"] & (df["amount"] > large_donation)).sum() / L3_len

        row["pct_$_above_all"] = df.loc[(df["amount"] > large_donation), "amount"].sum() / total_all
        row["pct_$_above_L3"] = df.loc[(df["last_3_years"] & (df["amount"] > large_donation)), "amount"].sum() / total_L3

        row["avg_donation_all"] = df["amount"].mean()
        row["avg_donation_L3"] = df.loc[df["last_3_years"], "amount"].mean()

        amt_non1a_all = df.loc[(df["d2_part"] != "1A"), "amount"].sum()
        amt_non1a_L3 = df.loc[((df["d2_part"] != "1A") & df["last_3_years"]) , "amount"].sum()
        row["amt_non1a_all"] = amt_non1a_all
        row["amt_non1a_L3"] = amt_non1a_L3

        row["pct_c_non1a_all"] = (df["d2_part"] != "1A").sum() / total_len
        row["pct_c_non1a_L3"] = (df["last_3_years"] & (df["d2_part"] != "1A")).sum() / L3_len

        row["pct_$_non1a_all"] = amt_non1a_all / total_all
        row["pct_$_non1a_L3"] = amt_non1a_L3 / total_L3

        amt_nofirst_all = df.loc[df["first_name"].isna(), "amount"].sum()
        amt_nofirst_L3 = df.loc[(df["first_name"].isna() & df["last_3_years"]) , "amount"].sum()
        row["amt_nofirst_all"] = amt_nofirst_all
        row["amt_nofirst_L3"] = amt_nofirst_L3

        row["pct_c_nofirst_all"] = df["first_name"].isna().sum() / total_len
        row["pct_c_nofirst_L3"] = (df["last_3_years"] & df["first_name"].isna()).sum() / L3_len

        row["pct_$_nofirst_all"] = amt_nofirst_all / total_all
        row["pct_$_nofirst_L3"] = amt_nofirst_L3 / total_L3

        amt_entity_all = df.loc[df["last_name"].str.contains(keywords, case=False), "amount"].sum()
        amt_entity_L3 = df.loc[(df["last_name"].str.contains(keywords, case=False) & df["last_3_years"]) , "amount"].sum()
        row["amt_entity_all"] = amt_entity_all
        row["amt_entity_L3"] = amt_entity_L3

        row["pct_c_entity_all"] = df["last_name"].str.contains(keywords, case=False).sum() / total_len
        row["pct_c_entity_L3"] = (df["last_3_years"] & df["last_name"].str.contains(keywords, case=False)).sum() / L3_len
        
        row["pct_$_entity_all"] = amt_entity_all / total_all
        row["pct_$_entity_L3"] = amt_entity_L3 / total_L3

        amt_allcond_all = df.loc[((df["d2_part"] != "1A") & (df["first_name"].isna()) & (df["last_name"].str.contains(keywords, case=False))), "amount"].sum()
        amt_allcond_L3 = df.loc[((df["d2_part"] != "1A") & (df["first_name"].isna()) & (df["last_name"].str.contains(keywords, case=False)) & df["last_3_years"]) , "amount"].sum()
        row["amt_allcond_all"] = amt_allcond_all
        row["amt_allcond_L3"] = amt_allcond_L3

        row["pct_c_allcond_all"] = ((df["d2_part"] != "1A") & (df["first_name"].isna()) & (df["last_name"].str.contains(keywords, case=False))).sum() / total_len
        row["pct_c_allcond_L3"] = ((df["d2_part"] != "1A") & (df["first_name"].isna()) & (df["last_name"].str.contains(keywords, case=False)) & df["last_3_years"]).sum() / L3_len
        
        row["pct_$_allcond_all"] = amt_allcond_all / total_all
        row["pct_$_allcond_L3"] = amt_allcond_L3 / total_L3

        amt_IL_all = df.loc[(df["state"] == "IL"), "amount"].sum()
        amt_IL_L3 = df.loc[((df["state"] == "IL") & df["last_3_years"]) , "amount"].sum()
        row["amt_IL_all"] = amt_IL_all
        row["amt_IL_L3"] = amt_IL_L3

        row["pct_c_IL_all"] = (df["state"] == "IL").sum() / total_len
        row["pct_c_IL_L3"] = (df["last_3_years"] & (df["state"] == "IL")).sum() / L3_len

        row["pct_$_IL_all"] = amt_IL_all / total_all
        row["pct_$_IL_L3"] = amt_IL_L3 / total_L3

        row["yrs_since_first"] = pd.Timestamp.today().year - pd.to_datetime(df["received_date"]).min().year

        row["yrs_since_last"] = pd.Timestamp.today().year - pd.to_datetime(df["received_date"]).max().year

        # Step 3: write to a row of the CSV
        writer.writerow(row)
    print("working names: ", working_names)
    print("working name percentage: ", (working_names / total_names)*100)