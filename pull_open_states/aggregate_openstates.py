import pandas as pd
import exploration.explore as ex
import matplotlib as plot
import re

# Create all_data object - dictionary with all sub-tables

def main():
    all_data = ex.get_all_datasets()

    # Load primary dataset
    df = all_data["bills"]
    # Filter down to only 'bills'
    df = df[df["classification"].apply(lambda x: "bill" in x)]

    # Load secondary datasets to join on
    bill_abstracts = all_data["bill_abstracts"]
    bill_actions = all_data["actions"]
    bills_sponsorships = all_data["bill_sponsorships"]
    #bill_organizations = all_data["organizations"]
    #bill_vote_counts = all_data["vote_counts"]
    #bill_votes = all_data["votes"]
    #bill_vote_people = all_data["vote_people"]

    # Merge Bills and Bill Abstracts
    df = df.merge(bill_abstracts, how = "inner", left_on = "id", right_on = "bill_id")  # (22782, 12)
    df = df.rename(columns = {"id_x": "id"})
    df = df.drop(columns = ["id_y", "bill_id"])

    # Add summary of actions to DF
    bill_actions["date"] = pd.to_datetime(bill_actions["date"])

    # Find dates of relevant bill milestones
    first_reading = bill_actions[bill_actions["classification"].apply(lambda x: "reading-1" in x)][["bill_id", "date"]]
    first_reading = first_reading.groupby("bill_id")["date"].min()
    first_reading = first_reading.reset_index()
    first_reading = first_reading.rename(columns = {"date": "first_reading_date"})

    first_referral = bill_actions[bill_actions["classification"].apply(lambda x: "referral-committee" in x)][["bill_id", "date"]]
    first_referral = first_referral.groupby("bill_id")["date"].min()
    first_referral = first_referral.reset_index()
    first_referral = first_referral.rename(columns = {"date": "first_committee_referral_date"})

    first_committee_passage = bill_actions[bill_actions["classification"].apply(lambda x: "committee-passage" in x)][["bill_id", "date"]]
    first_committee_passage = first_committee_passage.groupby("bill_id")["date"].min()
    first_committee_passage = first_committee_passage.reset_index()
    first_committee_passage = first_committee_passage.rename(columns = {"date": "first_committee_passage_date"})

    #key_dates = first_reading.merge(first_referral, how = "inner", left_on = "bill_id", right_on = "bill_id")
    #key_dates = key_dates.merge(first_committee_passage, how = "inner", left_on = "bill_id", right_on = "bill_id")


    actions_summary = bill_actions.groupby("bill_id").agg(
        first_action = ("date", "min"),
        last_action = ("date", "max"),
        num_actions = ("id", "count"),
        amendment_introductions = ("classification", lambda x: x.apply(lambda classif: "amendment-introduction" in classif).sum()),
        num_readings = ("classification", lambda x: x.apply(lambda classif: "reading" in classif).sum()),
        committee_passages = ("classification", lambda x: x.apply(lambda classif: "committee-passage" in classif).sum()),
        passed_first_chamber = ("classification", lambda x: x.apply(lambda classif: bool(re.search(r"'passage'", classif))).any()),
        passed_full_legislature = ("classification", lambda x: x.apply(lambda classif: "executive-receipt" in classif).any()),
        became_law = ("classification", lambda x: x.apply(lambda classif: "became-law" in classif).any()),
        vetoed = ("classification", lambda x: x.apply(lambda classif: "veto" in classif).any())
    ).sort_values(by = "num_actions", ascending=False)

    actions_summary = actions_summary.merge(first_reading, how = "left", on = "bill_id")
    actions_summary = actions_summary.merge(first_referral, how = "left", on = "bill_id")
    actions_summary = actions_summary.merge(first_committee_passage, how = "left", on = "bill_id")

    df = df.merge(actions_summary, how="inner", left_on="id", right_on="bill_id")

    # Add summary of sponsors to DFs
    sponsors_summary = bills_sponsorships.groupby("bill_id").agg(
        num_sponsors = ("id", "count"))

    primary_sponsors = bills_sponsorships["primary"] == True

    primary_sponsors_summary = bills_sponsorships[primary_sponsors].groupby("bill_id").agg(
        primary_sponsor_1 = ("name", "min"),
        primary_sponsor_2 = ("name", "max"))

    primary_sponsors_summary["num_primary_sponsors"] = 2  # For bills with only 1 primary sponsor, clear out primary_sponsor_2
    primary_sponsors_summary.loc[primary_sponsors_summary["primary_sponsor_2"] == 
                                 primary_sponsors_summary["primary_sponsor_1"], "num_primary_sponsors"] = 1
    primary_sponsors_summary.loc[primary_sponsors_summary["primary_sponsor_2"] == 
                                 primary_sponsors_summary["primary_sponsor_1"], "primary_sponsor_2"] = pd.NA

    sponsors_summary = sponsors_summary.merge(primary_sponsors_summary, 
                                              how="inner", left_on="bill_id", right_on="bill_id")
    df = df.merge(sponsors_summary, how="inner", left_on="id", right_on="bill_id")
    #df = df.drop(columns = ["id_y", "bill_id_x", "bill_id_y"])

    # Adding an action timeframe column
    df["first_to_last_action_time"] = df["last_action"] - df["first_action"]
    df["time_to_first_reading"] = df["first_reading_date"] - df["first_action"]
    df["time_to_first_committee_referral"] = df["first_committee_referral_date"] - df["first_action"]
    df["time_to_first_committee_passage"] = df["first_committee_passage_date"] - df["first_action"]

    # Pulling the first word out of the abstract
    df["abstract_action"] = df["abstract"].str.split().str[0].str.lower()

    df.to_csv("pull_open_states/intermediate_data/openstates_cleaned.csv")

    return df

if __name__ == "__main__":
    main()