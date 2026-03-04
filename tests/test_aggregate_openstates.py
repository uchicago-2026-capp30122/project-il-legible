import pytest
from pathlib import Path
import exploration.explore as ex

from pull_open_states.aggregate_openstates import summarize_actions
from pull_open_states.clean_name_column import general_name_cleaning

#@pytest.fixture
def openstates_data_sample():
    all_data = ex.get_all_datasets()

    # Get sample of 10 relevant bills
    bills = all_data["bills"]
    bills = bills[bills["classification"].apply(lambda x: "bill" in x)]
    bills = bills.sort_values("id")[:10]

    bill_actions = all_data["actions"].sort_values("bill_id")[:200]
    bill_sponsorships = all_data["bill_sponsorships"].sort_values("bill_id")[:200]

    return (bills, bill_actions, bill_sponsorships)


def test_summarize_actions():
     _, bill_actions, _ = openstates_data_sample()
     bills_summary = summarize_actions(bill_actions)
     assert bill_actions.shape == (200, 7)
     assert bill_actions["bill_id"].nunique() == 14




def test_automated_name_cleaning():
    """Test that cleaning works as expected for specific names."""
    assert general_name_cleaning("Marcus C. Evans, Jr.") == "Marcus Evans Jr"
    assert general_name_cleaning("Christopher \"C.D.\" Davidsmeyer") == "Christopher Davidsmeyer"

