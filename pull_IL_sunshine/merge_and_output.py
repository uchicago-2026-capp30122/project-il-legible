"""
This file adds statistics on bills to each sponsor and outputs the final dataset.
"""

import pandas as pd

def aggregate_bill_stats(bills: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates statistics on each legislator's activity, covering number of bills
    introduced and the passage rate of those bills. Some bills (about 15%) have 
    two primary sponsors listed, and this functions gives credit to both.

    Inputs:
        bills (pd.DataFrame): A dataframe with data on each bill
    
    Outputs:
        A new DataFrame with aggregated legislator stats, with one row for each
        primary sponsor across both legislative sessions.
    """
    sponsor_1 = bills.groupby("primary_sponsor_1_clean").agg({
        "organization_classification": "first", 
        "id" : "count",
        "passed_full_legislature" : "sum"
    }).reset_index()

    sponsor_2 = bills.groupby("primary_sponsor_2_clean").agg({
        "organization_classification": "first", 
        "id" : "count",
        "passed_full_legislature" : "sum"
    }).reset_index()

    # Merge both Primary Sponsor columns into one DataFrame
    df = sponsor_1.merge(sponsor_2, how = "left", left_on = "primary_sponsor_1_clean", 
                         right_on = "primary_sponsor_2_clean")

    # Fill NAs with 0s for upcoming calculations
    df = df.fillna(0)

    bill_agg = pd.DataFrame()
    bill_agg["name"] = df["primary_sponsor_1_clean"]
    bill_agg["num_bills"] = df["id_x"] + df["id_y"]
    bill_agg["num_bills"]  = bill_agg["num_bills"].astype(int)
    bill_agg["organization_classification"] = df["organization_classification_x"]

    bill_agg["bills_passed"] = df["passed_full_legislature_x"] + df["passed_full_legislature_y"]
    bill_agg["bills_passed"] = bill_agg["bills_passed"].astype(int)

    bill_agg["pct_bills_passed"] = bill_agg["bills_passed"] / bill_agg["num_bills"]

    return bill_agg


def calculate_legislator_effectiveness(sponsors: pd.DataFrame) -> pd.DataFrame:
    """
    Add columns scoring legislators based on their number of bills introduced,
    passage rate of those bills, and a combined ranking averaging the two.
    Uses percentiles for both calculations.

    Inputs:
        sponsors (pd.DataFrame): A dataframe with sponsor data
    
    Outputs:
        An new DataFrame including the new effectiveness columns
    """
    sponsors["bills_introduced_percentile"] = sponsors["num_bills"].rank(pct=True)
    sponsors["passage_rate_percentile"] = sponsors["pct_bills_passed"].rank(pct=True)
    sponsors["effectiveness_score"] = (sponsors["bills_introduced_percentile"] +
                                        sponsors["passage_rate_percentile"]) / 2

    return sponsors


def output_final_sponsors_csv(sponsors_cleaned: pd.DataFrame) -> None:
    """
    Generates and saves a consolidated CSV with all key and cleaned sponsor data.

    Inputs:
        sponsors_cleaned (pd.DataFrame): A dataframe with cleaned and summarized 
        sponsor data.
    
    Outputs:
        None. Directly saves a CSV
    """
    cols_final = ["name", "organization_classification", "donation_count_all", 
                    "donation_count_L3", "total_all", "total_L3", "pct_c_above_all",
                    "pct_c_above_L3", "avg_donation_all", "avg_donation_L3",
                    "amt_allcond_all", "amt_allcond_L3", "pct_c_allcond_all",
                    "pct_c_allcond_L3", "pct_c_IL_all", "pct_c_IL_L3",
                    "num_bills", "pct_bills_passed",
                    "first_donation_year", "effectiveness_score"]

    sponsors_cleaned[cols_final].to_csv("final_data/sponsors_test.csv")


def main():
    donations = pd.read_csv("pull_IL_sunshine/intermediate_data/donation_stats.csv")
    bills = pd.read_csv("pull_open_states/intermediate_data/openstates_w_names.csv")

    bill_agg = aggregate_bill_stats(bills)
    sponsors = pd.merge(donations, bill_agg, how = "left", on = "name")
    sponsors = calculate_legislator_effectiveness(sponsors)
    
    output_final_sponsors_csv(sponsors)


if __name__ == "__main__":
    main()