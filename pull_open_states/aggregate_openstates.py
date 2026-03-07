import pandas as pd
import exploration.explore as ex
import re
from pathlib import Path


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load three bills-related datasets to use in building the summarized dataset.

    Inputs:
        None
    
    Returns:
        bills (pd.DataFrame): Contains basic data on each bill, with one row
            per bill
        bill_actions (pd.DataFrame): Contains all actions associated with each
            bill, with multiple rows per bill
        bill_sponsorships (pd.DataFrame): Contains all sponsors associated with
            each bill, with multiple rows per bill
    """
    all_data = ex.get_all_datasets()

    bills = all_data["bills"]
    # Filter down to only relevant types of legislation
    bills = bills[bills["classification"].apply(lambda x: "bill" in x)]

    bill_actions = all_data["actions"]
    bill_sponsorships = all_data["bill_sponsorships"]

    return (bills, bill_actions, bill_sponsorships)


def summarize_actions(bill_actions: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes a DataFrame with many-to-one actions-to-bills into one-to-one
    relationships for key fields.

    Inputs:
        bill_actions (pd.DataFrame): Contains every action associated with bills
    
    Outputs:
        A DataFrame with one-to-one mapping of bills to summarized actions
    """
    actions_summary = bill_actions.groupby("bill_id").agg(
        first_action = ("date", "min"),
        committee_passages = ("classification", lambda x: x.apply(lambda classif: "committee-passage" in classif).sum()),
        referred_to_committee = ("classification", lambda x: x.apply(lambda classif: "referral-committee" in classif).any()),
        passed_first_chamber = ("classification", lambda x: x.apply(lambda classif: bool(re.search(r"'passage'", classif))).any()),
        passed_full_legislature = ("classification", lambda x: x.apply(lambda classif: "executive-receipt" in classif).any()),
        became_law = ("classification", lambda x: x.apply(lambda classif: "became-law" in classif).any()))

    return actions_summary


def summarize_sponsors(bill_sponsorships: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes a DataFrame with many-to-one sponsors-to-bills into one-to-one
    relationships for key fields.

    Inputs:
        bill_actions (pd.DataFrame): Contains every action associated with bills
    
    Outputs:
        A DataFrame with one-to-one mapping of bills to summarized sponsors
    """
    sponsors_stats = bill_sponsorships.groupby("bill_id").agg(
        num_sponsors = ("id", "count"))

    primary_sponsors = bill_sponsorships["primary"] == True
    primary_sponsors_summary = bill_sponsorships[primary_sponsors].groupby("bill_id").agg(
        primary_sponsor_1 = ("name", "min"),
        primary_sponsor_2 = ("name", "max"))

    # For bills with only 1 primary sponsor, clear primary_sponsor_2
    primary_sponsors_summary.loc[primary_sponsors_summary["primary_sponsor_2"] == 
                                 primary_sponsors_summary["primary_sponsor_1"], "primary_sponsor_2"] = pd.NA

    sponsors_summary = sponsors_stats.merge(primary_sponsors_summary, 
                                              how="inner", left_on="bill_id", right_on="bill_id")

    return sponsors_summary


def merge_datasets(bills: pd.DataFrame, actions_summary: pd.DataFrame, 
                   sponsors_summary: pd.DataFrame) -> pd.DataFrame:
    """
    Create a final combined dataset, with one row for each bill, and with all
    associated summary fields.

    Inputs:
        bills (pd.DataFrame): Basic identifiers for each bill
        actions_summary: Key action stats, summarized for each bill
        sponsors_summary: Key sponsorship stats, summarized for each bill
    
    Outputs:
        A single DataFrame with all bills and all relevant summary stats
    """
    
    intermediate_df = bills.merge(actions_summary, how="inner", left_on="id", right_on="bill_id")
    final_df = intermediate_df.merge(sponsors_summary, how="inner", left_on="id", right_on="bill_id")

    return final_df


def main():
    bills, bill_actions, bill_sponsorships = load_datasets()
    actions_summary = summarize_actions(bill_actions)
    sponsors_summary = summarize_sponsors(bill_sponsorships)

    final_df = merge_datasets(bills, actions_summary, sponsors_summary)

    # Write to CSV
    filepath = Path("pull_open_states/intermediate_data/openstates_cleaned")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(filepath)


if __name__ == "__main__":
    main()