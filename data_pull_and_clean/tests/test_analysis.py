import pytest
import pandas as pd
from data_pull_and_clean.pull_IL_sunshine.merge_and_output import (
    calculate_legislator_effectiveness,
)


@pytest.fixture
def sample_legislator_data():
    """
    Create a DataFrame containing names, bill counts, pct_bills_passed for a
    small set of legislators to use in testing.

    Test set:
        - None: Zero volume, Zero passage rate
        - Low: Low volume, Mid passage rate
        - Medium: Mid volume, Mid passage rate
        - High: High volume, High passage rate
        - All: Highest volume, Highest passage rate
    """

    data = {
        "name": [
            "legislator_none",
            "legislator_low",
            "legislator_medium",
            "legislator_high",
            "legislator_highest",
        ],
        "num_bills": [0, 10, 20, 50, 55],
        "pct_bills_passed": [0.0, 0.1, 0.1, 0.15, 0.2],
    }
    return pd.DataFrame(data)


def test_bills_introduced_percentiles(sample_legislator_data):
    """
    Test the logic used to determine Bills Introduced percentiles (a component
    of Legislator Effectivess Scores) on a small set of sample data.
    """
    result = calculate_legislator_effectiveness(sample_legislator_data)
    result_indexed = result.set_index("name")

    assert result_indexed.loc["legislator_highest"]["bills_introduced_percentile"] == 1
    assert result_indexed.loc["legislator_low"]["bills_introduced_percentile"] == 0.4


def test_passage_rate_percentiles(sample_legislator_data):
    """
    Test the logic used to determine Bill Passage Rate percentiles (a component
    of Legislator Effectivess Scores) on a small set of sample data.
    """
    result = calculate_legislator_effectiveness(sample_legislator_data)
    result_indexed = result.set_index("name")

    assert result_indexed.loc["legislator_high"]["passage_rate_percentile"] == 0.8
    assert result_indexed.loc["legislator_none"]["passage_rate_percentile"] == 0.2


def test_final_effectiveness_order(sample_legislator_data):
    """
    Test the logic used to determine final Legislator Effectiveness scores
    on a small set of sample data.
    """
    result = calculate_legislator_effectiveness(sample_legislator_data)
    sorted_result = result.sort_values(by="effectiveness_score", ascending=False)

    # Check order of sorted results against expected order
    expected_order = [
        "legislator_highest",
        "legislator_high",
        "legislator_medium",
        "legislator_low",
        "legislator_none",
    ]
    assert list(sorted_result["name"]) == expected_order
