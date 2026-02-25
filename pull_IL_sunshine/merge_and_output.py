"""
This file adds statistics on bills to each sponsor and outputs the final dataset.
"""

import pandas as pd

donations = pd.read_csv("pull_IL_sunshine/intermediate_data/donation_stats.csv")


# Keep specific columns
columns_to_keep = ["Name", "donation_count_all", "donation_count_L3",
                   "total_all", "total_L3", "pct_c_above_all", "pct_c_above_L3",
                   "avg_donation_all", "avg_donation_L3", "pct_$_non1a_all",
                   "pct_$_non1a_L3", "pct_$_IL_all", "pct_$_IL_L3"]
donations[columns_to_keep].to_csv("final_data/sponsors.csv")
