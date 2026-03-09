import pytest
import exploration.explore as ex

from pull_open_states.aggregate_openstates import summarize_actions, summarize_sponsors
from pull_open_states.clean_name_column import general_name_cleaning

@pytest.fixture
def get_actions_sample():
    """Get fixed set of 200 bill actions to use in testing."""

    actions = ex.get_actions()
    actions = actions.sort_values("bill_id")[:200]
    return actions


@pytest.fixture
def get_sponsors_sample():
    """Get fixed set of 200 bill sponsors to use in testing."""

    sponsors = ex.get_sponsors()
    sponsors = sponsors.sort_values("bill_id")[:200]
    return sponsors


def test_summarize_actions_shape(get_actions_sample):
    """Test the shape of the output from Bill Actions summarization logic."""
    bills_summary = summarize_actions(get_actions_sample)
    assert bills_summary.shape == (14, 6)


def test_summarize_actions_values(get_actions_sample):
    """Test two specific values from Bill Actions summarization logic."""
    actions_summary = summarize_actions(get_actions_sample)
    assert actions_summary.loc["ocd-bill/002a4c9d-e0bc-4f58-8f93-4f6656cf73d5"]["passed_full_legislature"] == True
    assert actions_summary["committee_passages"].sum() == 3


def test_summarize_sponsors_shape(get_sponsors_sample):
    """Test the shape of the output from Bill Sponsors summarization logic."""
    sponsors_summary = summarize_sponsors(get_sponsors_sample)
    assert sponsors_summary.shape == (66, 3)


def test_summarize_sponsors_values(get_sponsors_sample):
    """Test two specific values from Bill Sponsors summarization logic."""
    sponsors_summary = summarize_sponsors(get_sponsors_sample)
    assert sponsors_summary.loc["ocd-bill/00a8be44-1eda-4f58-9a89-26a72911b601"]["num_sponsors"] == 14
    assert sponsors_summary["primary_sponsor_2"].notna().sum() == 10


def test_automated_name_cleaning():
    """
    Test that regex-based cleaning works as expected for two specific names.
    """
    assert general_name_cleaning("Marcus C. Evans, Jr.") == "Marcus Evans Jr"
    assert general_name_cleaning("Christopher \"C.D.\" Davidsmeyer") == "Christopher Davidsmeyer"

