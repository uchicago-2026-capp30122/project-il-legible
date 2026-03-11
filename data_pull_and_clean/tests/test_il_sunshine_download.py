import pytest

from data_pull_and_clean.pull_IL_sunshine.Illinois_Sunshine_donations_pull import (
    match_sponsor_to_candidate,
    get_committee_ids,
    download_donations,
)


def test_sponsor_to_candidate():
    """Test conversion from a Bill sponsor to an IL Sunshine candidate ID."""
    assert match_sponsor_to_candidate("Don Harmon") == [16940, 40755, 16939]
    assert match_sponsor_to_candidate("Tony McCombie") == [45960, 19156, 34424]


def test_get_committee_ids():
    """Test conversion from an IL Sunshine candidate ID to a fundraising committee ID."""
    # Don Harmon - expecting 3 committees
    assert sorted(get_committee_ids([16940, 40755, 16939])) == [
        "16283",
        "34378",
        "34379",
    ]
    # Tony McCombie - expecting 1 committee
    assert get_committee_ids([45960, 19156, 34424]) == ["31997"]


def test_download_donations():
    """Test downloading donation records using a fundraising committee ID."""
    mccombie_download = download_donations("31997")
    assert len(list(mccombie_download)) >= 3000
