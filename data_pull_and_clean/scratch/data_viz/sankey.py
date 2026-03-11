import pandas as pd
import plotly.graph_objects as go

FILENAME = "../final_data/bills.csv"
main_df = pd.read_csv(FILENAME)
MAIN_COLOR = "maroon"


def bill_progress_sankey(df):

    df["first_action"] = pd.to_datetime(df["first_action"], errors="coerce")
    df["first_committee_referral_date"] = pd.to_datetime(
        df["first_committee_referral_date"], errors="coerce"
    )

    introduced = df["first_action"].notna()
    referred_to_committee = introduced & df["first_committee_referral_date"].notna()
    passed_committee = referred_to_committee & (df["committee_passages"] > 0)
    passed_first_chamber = passed_committee & df["passed_first_chamber"]
    passed_full_legislature = passed_first_chamber & df["passed_full_legislature"]
    became_law = passed_full_legislature & df["became_law"]

    n_intro_to_referred = referred_to_committee.sum()
    n_referred_to_committee_pass = passed_committee.sum()
    n_committee_to_first_chamber = passed_first_chamber.sum()
    n_first_chamber_to_full = passed_full_legislature.sum()
    n_full_chamber_to_law = became_law.sum()

    labels = [
        "Introduced",
        "Referred to Committee",
        "Passed Committee",
        "Passed First Chamber",
        "Passed Full Legislature",
        "Became Law",
    ]

    node_map = {}
    for i, label in enumerate(labels):
        node_map[label] = i

    sources = [
        node_map["Introduced"],
        node_map["Referred to Committee"],
        node_map["Passed Committee"],
        node_map["Passed First Chamber"],
        node_map["Passed Full Legislature"],
    ]

    targets = [
        node_map["Referred to Committee"],
        node_map["Passed Committee"],
        node_map["Passed First Chamber"],
        node_map["Passed Full Legislature"],
        node_map["Became Law"],
    ]

    values = [
        n_intro_to_referred,
        n_referred_to_committee_pass,
        n_committee_to_first_chamber,
        n_first_chamber_to_full,
        n_full_chamber_to_law,
    ]

    node_x = [0.0, 0.17, 0.34, 0.51, 0.68, 0.9]
    node_y = [0.5, 0.5, 0.4, 0.47, 0.5, 0.5]

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="fixed",
                node=dict(
                    pad=20,
                    thickness=20,
                    line=dict(color=MAIN_COLOR, width=0.5),
                    label=labels,
                    x=node_x,
                    y=node_y,
                    hovertemplate="%{label}<extra></extra>",
                ),
                link=dict(source=sources, target=targets, value=values),
            )
        ]
    )

    fig.update_layout(
        title="Bill Progress Through Legislative Milestones",
        font_size=12,
        width=1400,
        height=600,
    )

    return fig


if __name__ == "__main__":
    sankey = bill_progress_sankey(main_df)
    sankey.write_html("bill_progress_sankey.html")
    print("Saved chart to bill_progress_sankey.html")
