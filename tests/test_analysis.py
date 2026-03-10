import pytest
import pandas as pd
from pull_IL_sunshine.merge_and_output import calculate_legislator_effectiveness


@pytest.fixture
def sample_legislator_data():
    """
    Create a DataFrame containing names, bill counts, pct_bills_passed for a
    small set of legislators to use in testing.
    """

    data = {
        "name": [
            "Legislator_None",
            "Legislator_Low",
            "Legislator_Medium",
            "Legislator_High",
            "Legislator_All",
        ],
        "num_bills": [0, 10, 20, 50, 50],
        "pct_bills_passed": [0.0, 0.1, 0.1, 0.1, 0.2],
    }
    return pd.DataFrame(data)


def test_legislator_effectiveness(sample_legislator_data):
    """
    Test the logic used to determine Legislator Effectiveness on a small set of
    sample data.

    Expected Rankings (Highest Score to Lowest Score):
        Legislator_All
        Legislator_High
        Legislator_Medium
        Legislator_Low
        Legislator_None

    """
    result = calculate_legislator_effectiveness(sample_legislator_data)
    # Sort based on effectiveness score, largest to smallest
    result = result.sort_values(by="effectiveness_score", ascending=False)
    # Check order of sorted results against expected order
    assert list(result["name"]) == [
        "Legislator_All",
        "Legislator_High",
        "Legislator_Medium",
        "Legislator_Low",
        "Legislator_None",
    ]
