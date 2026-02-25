"""
This file adds statistics on bills to each sponsor and outputs the final dataset.
"""

import pandas as pd

donations = pd.read_csv("pull_IL_sunshine/intermediate_data/donation_stats.csv")
bills = pd.read_csv("pull_open_states/intermediate_data/openstates_w_names.csv")

# Merge Chamber into donation data
bill_agg = bills.groupby("primary_sponsor_1_clean").agg({
    "organization_classification" : "first", 
    "id" : "count",
    "passed_full_legislature" : "sum"
    }).reset_index()

bill_agg = bill_agg.rename(columns = {"primary_sponsor_1_clean" : "name",
                                      "id" : "num_bills",
                                      "passed_full_legislature" : "bills_passed"})
bill_agg["pct_bills_passed"] = bill_agg["bills_passed"] / bill_agg["num_bills"]

sponsors = pd.merge(donations, bill_agg, how = "left", on = "name")

# Keep specific columns
columns_to_keep = ["name", "organization_classification", "donation_count_all", 
                   "donation_count_L3", "total_all", "total_L3", "pct_c_above_all",
                   "pct_c_above_L3", "avg_donation_all", "avg_donation_L3",
                   "pct_$_non1a_all", "pct_$_non1a_L3", "pct_$_IL_all",
                   "pct_$_IL_L3", "num_bills", "bills_passed", "pct_bills_passed",
                   "yrs_since_first", "yrs_since_last"]

# Output final dataset
sponsors[columns_to_keep].to_csv("final_data/sponsors.csv")
