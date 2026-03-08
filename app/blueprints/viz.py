from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor, Bill
from sqlalchemy import select
import pandas as pd
import altair as alt
import plotly.graph_objects as go

bp = Blueprint('viz', __name__)

COLORS = {
    "blue": "#1A3C8C",
    "yellow": "#EBE973",
    "red": "#8C303C",
    "charcol": "#404437",
    "grey": "#E5E7EA",
    "orange": "#FF8050"
}
SIZE = 60

def total_donation_history(sponsors):
    df = pd.read_sql(sponsors, db.engine)
    chart = (
        alt.Chart(df)
        .mark_bar(color=COLORS["red"])
        .transform_bin(
            ["bin_start", "bin_end"],
            field="avg_donation_all",
            bin=alt.Bin(maxbins=50))
        .encode(
            x = alt.X(
                "bin_start:Q",
                bin="binned",
                title="Total Donation Amount ($)",
                axis=alt.Axis(
                    tickMinStep=2_000_000,
                    labelFontSize=12,
                    titleFontSize=15,
                    titlePadding=15,
                    labelExpr="datum.value % 10000000 === 0 ? format(datum.value, '~s') : ''")
                    ),
            x2="bin_end:Q",
            y = alt.Y(
                'count()',
                title = "Number of Sponsors",
                axis=alt.Axis(grid=False, labelFontSize=12, titleFontSize=15,
                              titlePadding=10)),
            tooltip=[
                alt.Tooltip("count()", title="Number of Sponsors", format=","),
                alt.Tooltip("bin_start:Q", title="Total Donations From", format="$,.0f"),
                alt.Tooltip("bin_end:Q", title="To", format="$,.0f")
            ],
            )
        .properties(width="container")
    )
    
    return chart

def num_bills_bar(sponsor_name: str, sponsors):
    """
    Create a bar graph showing the number of bills introduced by a specific legislator
    compared to an average.

    Inputs:
        sponsor_name: name of specific sponsor
        sponsors: query object of sponsor information
    
    Returns:
        An Altair Chart
    """
    df = pd.read_sql(sponsors, db.engine)
    
    legislator_bills = df[df["name"] == sponsor_name]["num_bills"].mean()
    median_bills = df["num_bills"].median()

    legislator_df = pd.DataFrame({
        "names": ["Median Sponsor", sponsor_name],
        "num_bills": [median_bills, legislator_bills]
    })
    
    chart=(
        alt.Chart(legislator_df)
        .mark_bar(color=COLORS["blue"])
        .encode(
            x = alt.X("names", title="",
                        axis=alt.Axis(
                            labelAngle=0,
                            labelFontSize=15,
                            grid=False)),
            y = alt.Y("num_bills", title="",
                        axis=alt.Axis(
                            labelFontSize=12,
                            grid=False)),
            tooltip=[
                alt.Tooltip("names", title=" "),
                alt.Tooltip("num_bills:Q", title="Count", format=",")
                ]
                )
        .properties(
            width = 300,
            height = 400
        )
    )

    text = chart.mark_text(
        dy=-10,
        fontSize=17,
        color=COLORS["blue"]
        ).encode(
        text=alt.Text("num_bills:Q", format=",")
        )

    return chart + text

def bill_success_legislator(name: str, sponsors) -> alt.Chart:
    """
    Create a pie chart (my apologies in advance) showing the number of bills 
    introduced by a specific legislator compared to an average.

    Inputs:
        df: Dataframe with legislator and bill data
        name: Legislator's name
    
    Returns:
        An Altair Chart
    """
    df = pd.read_sql(sponsors, db.engine)
    legislator_passed = df[df["name"] == name]["pct_bills_passed"].mean()

    bill_success_df = pd.DataFrame({
        "Legend": ["Passed", "Failed"],
        "num_bills": [legislator_passed, 1 - legislator_passed]
    })

    base=(
        alt.Chart(bill_success_df)
        .encode(
            theta="num_bills",
            color=alt.Color(
                "Legend",
                scale=alt.Scale(
                    domain=["Passed", "Failed"],
                    range=[COLORS["blue"], COLORS["grey"]]
                    ),
                legend=None
                ),
            tooltip=[
                alt.Tooltip("Legend", title="Outcome"),
                alt.Tooltip("num_bills:Q", title="Percent", format=".2%")
                ])   
        .properties(
            width=250)
    )

    pie = base.mark_arc(color=COLORS["blue"])

    return pie

def average_donation_history(sponsors):
    df = pd.read_sql(sponsors, db.engine)
    chart = (
        alt.Chart(df)
        .transform_bin(
            ["bin_start", "bin_end"],
            field="avg_donation_all",
            bin=alt.Bin(maxbins=50))
        .mark_bar(color=COLORS["red"])
        .encode(
            x = alt.X(
                "bin_start:Q",
                bin="binned",
                title="Average Donation Amount ($)",
                axis=alt.Axis(format="~s",
                    labelFontSize=12,
                    titleFontSize=15,
                    titlePadding=15)
                ),
            x2="bin_end:Q",
            y = alt.Y(
                'count()',
                title = "Number of Sponsors",
                axis=alt.Axis(grid=False,
                    labelFontSize=12,
                    titleFontSize=15,
                    titlePadding=10)),
            tooltip=[
                alt.Tooltip("count()", title="Number of Sponsors", format=","),
                alt.Tooltip("bin_start:Q", title="Average Donation From", format="$,.0f"),
                alt.Tooltip("bin_end:Q", title="To", format="$,.0f")
            ],
                )
        .properties(width="container")
        )
    
    return chart

def bills_by_donations_scatter(sponsors):
    df = pd.read_sql(sponsors, db.engine)
    donation_choice = alt.param(
        name="DonationWindow",
        value="All time",
        bind=alt.binding_select(
            options=["All time", "Last 3 years"],
            name="Donations: "
            )
        )

    base = (
        alt.Chart(df)
        .add_params(donation_choice)
        .transform_calculate(
            donation_x=
            "DonationWindow == 'All time' ? datum.total_all : datum.total_L3"
            )
        )

    points=(
        base
        .mark_circle(size=SIZE, color=COLORS["blue"])
        .encode(
            x = alt.X("donation_x:Q", title="Total Donation Amount",
                    axis=alt.Axis(
                    grid=False,
                    labelFontSize=12,
                    titleFontSize=15,
                    titlePadding=15,
                    labelExpr="datum.value % 10000000 === 0 ? format(datum.value, '~s') : ''")),
            y = alt.Y("num_bills", title="Number of Bills Introduced",
                    axis=alt.Axis(
                    grid=False,
                    labelFontSize=12,
                    titleFontSize=15,
                    titlePadding=10)),
            tooltip=[
                alt.Tooltip("name", title="Legislator"),
                alt.Tooltip("total_all", title="All-time Donations", format="$,.0f"),
                alt.Tooltip("total_L3", title="Last 3 years Donations", format="$,.0f"),
                alt.Tooltip("num_bills", title="Bills Introduced", format=",")
            ],
            href="url:N"
            )
    )

    line = (
        base
        .transform_regression("donation_x", "num_bills")
        .mark_line(color="black")
        .encode(
            x = "donation_x:Q",
            y = "num_bills:Q"
        )
    )

    chart = (
        (points + line)
        .properties(width="container")
        .transform_calculate(
            url='/sponsors/' + alt.datum.id
        )
        .interactive()
    )

    return chart

def large_donation_barchart(name, sponsors, time):
    df = pd.read_sql(sponsors, db.engine)
    person = df[df["name"] == name].iloc[0]

    chart_df = pd.DataFrame({
        "category": [["Over", "$1,000"], ["Under", "$1,000"]],
        "name": ["Over $1,000", "Under $1,000"],
        "percent_all": [
            float(person["pct_c_above_all"]),
            1 - float(person["pct_c_above_all"])
        ],
        "percent_L3": [
            float(person["pct_c_above_L3"]),
            1 - float(person["pct_c_above_L3"])
        ],
        "count_all":[
            int(person["pct_c_above_all"] * person["donation_count_all"]),
            int((1 - float(person["pct_c_above_all"])) * person["donation_count_all"])
        ],
        "count_L3":[
            int(person["pct_c_above_L3"] * person["donation_count_L3"]),
            int((1 - float(person["pct_c_above_L3"])) * person["donation_count_L3"])
        ]
    })

    pct_selected = "percent_" + time
    count_selected = "count_" + time

    bars = (
        alt.Chart(chart_df)
        .mark_bar(color=COLORS["red"], size=30)
        .encode(
            x=alt.X(
                pct_selected + ":Q",
                title="",
                scale=alt.Scale(domain=[0,1]),
                axis=alt.Axis(grid=False, format=".0%",
                            labelFontSize=12,)
                ),
            y=alt.Y("category:N", title="",
                    axis=alt.Axis(ticks=False,
                                labelFontSize=15,
                                labelPadding=10)
                ),
            tooltip=[
                alt.Tooltip("name", title=" "),
                alt.Tooltip(pct_selected + ":Q", title="Percent", format=".0%"),
                alt.Tooltip(count_selected + ":Q", title="Count", format=",")
                ]
            )
        ).properties(
            width=300,
            height=200)
    
    labels = (
        alt.Chart(chart_df)
        .mark_text(
            align="left",
            dx=3,
            fontSize=15,
            color=COLORS["red"]
        )
        .encode(
            x=pct_selected + ":Q",
            y="category:N",
            text=alt.Text(pct_selected + ":Q", format=".0%")
        )
    )
    
    chart = (bars + labels)
        
    return chart

def entity_donation_barchart(name, sponsors, time):
    df = pd.read_sql(sponsors, db.engine)
    person = df[df["name"] == name].iloc[0]

    chart_df = pd.DataFrame({
        "category": [["From", "Entities"], ["From", "Individuals"]],
        "name": ["From Entities", "From Individuals"],
        "percent_all": [
            float(person["pct_c_allcond_all"]),
            1 - float(person["pct_c_allcond_all"])
        ],
        "percent_L3": [
            float(person["pct_c_allcond_L3"]),
            1 - float(person["pct_c_allcond_L3"])
        ],
        "count_all":[
            int(person["pct_c_allcond_all"] * person["donation_count_all"]),
            int((1 - float(person["pct_c_allcond_all"])) * person["donation_count_all"])
        ],
        "count_L3":[
            int(person["pct_c_allcond_L3"] * person["donation_count_L3"]),
            int((1 - float(person["pct_c_allcond_L3"])) * person["donation_count_L3"])
        ]
    })

    pct_selected = "percent_" + time
    count_selected = "count_" + time

    bars = (
        alt.Chart(chart_df)
        .mark_bar(color=COLORS["red"], size=30)
        .encode(
            x=alt.X(
                pct_selected + ":Q",
                title="",
                scale=alt.Scale(domain=[0,1]),
                axis=alt.Axis(grid=False, format=".0%",
                            labelFontSize=12,)
                ),
            y=alt.Y("category:N", title="",
                    axis=alt.Axis(ticks=False,
                                labelFontSize=15,
                                labelPadding=10)
                ),
            tooltip=[
                alt.Tooltip("name", title=" "),
                alt.Tooltip(pct_selected + ":Q", title="Percent", format=".0%"),
                alt.Tooltip(count_selected + ":Q", title="Count", format=",")
                ]
            )
        ).properties(
            width=300,
            height=200)
    
    labels = (
        alt.Chart(chart_df)
        .mark_text(
            align="left",
            dx=3,
            fontSize=15,
            color=COLORS["red"]
        )
        .encode(
            x=pct_selected + ":Q",
            y="category:N",
            text=alt.Text(pct_selected + ":Q", format=".0%")
        )
    )
    
    chart = (bars + labels)
        
    return chart

def in_state_donation_barchart(name, sponsors, time):
    df = pd.read_sql(sponsors, db.engine)
    person = df[df["name"] == name].iloc[0]

    chart_df = pd.DataFrame({
        "category": [["In", "State"], ["Out of", "State"]],
        "name": ["In-State", "Out-of-State"],
        "percent_all": [
            float(person["pct_c_IL_all"]),
            1 - float(person["pct_c_IL_all"])
        ],
        "percent_L3": [
            float(person["pct_c_IL_L3"]),
            1 - float(person["pct_c_IL_L3"])
        ],
        "count_all":[
            int(person["pct_c_IL_all"] * person["donation_count_all"]),
            int((1 - float(person["pct_c_IL_all"])) * person["donation_count_all"])
        ],
        "count_L3":[
            int(person["pct_c_IL_L3"] * person["donation_count_L3"]),
            int((1 - float(person["pct_c_IL_L3"])) * person["donation_count_L3"])
        ]
    })

    pct_selected = "percent_" + time
    count_selected = "count_" + time

    bars = (
        alt.Chart(chart_df)
        .mark_bar(color=COLORS["red"], size=30)
        .encode(
            x=alt.X(
                pct_selected + ":Q",
                title="",
                scale=alt.Scale(domain=[0,1]),
                axis=alt.Axis(grid=False, format=".0%",
                            labelFontSize=12,)
                ),
            y=alt.Y("category:N", title="",
                    axis=alt.Axis(ticks=False,
                                labelFontSize=15,
                                labelPadding=10)
                ),
            tooltip=[
                alt.Tooltip("name", title=" "),
                alt.Tooltip(pct_selected + ":Q", title="Percent", format=".0%"),
                alt.Tooltip(count_selected + ":Q", title="Count", format=",")
                ]
            )
        ).properties(
            width=300,
            height=200)
    
    labels = (
        alt.Chart(chart_df)
        .mark_text(
            align="left",
            dx=3,
            fontSize=15,
            color=COLORS["red"]
        )
        .encode(
            x=pct_selected + ":Q",
            y="category:N",
            text=alt.Text(pct_selected + ":Q", format=".0%")
        )
    )
    
    chart = (bars + labels)
        
    return chart

def bill_progress_sankey(bills):

    df = pd.read_sql(bills, db.engine)
    
    df["first_action"] = pd.to_datetime(df["first_action"], errors="coerce")

    introduced = df["first_action"].notna()
    referred_to_committee = introduced & df["referred_to_committee"]
    passed_committee = referred_to_committee & (df["committee_passages"] > 0)
    passed_first_chamber = passed_committee & df["passed_first_chamber"]
    passed_full_legislature = passed_first_chamber & df["passed_full_legislature"]
    became_law = passed_full_legislature & df["became_law"]

    n_introduced= introduced.sum()
    n_intro_to_referred = referred_to_committee.sum()
    n_not_referred = n_introduced - n_intro_to_referred
    n_referred_to_committee_pass = passed_committee.sum()
    n_committee_to_first_chamber = passed_first_chamber.sum()
    n_first_chamber_to_full = passed_full_legislature.sum()
    n_full_chamber_to_law = became_law.sum()
    


    labels = [
        "Introduced",
        "",
        "Referred to Committee",
        "Passed Committee",
        "Passed First Chamber",
        "Passed Full Legislature",
        "Became Law"
    ]

    node_colors= [
        "#80A6FD",
        "rgba(0,0,0,0)",
        "#4E82FD",
        "#3069EE",
        "#285ACE",
        "#2450B8",
        "#1A3C8C"
    ]

    link_colors= [
        "rgba(0,0,0,0)",
        "#E5E7EA",
        "#E5E7EA",
        "#E5E7EA",
        "#E5E7EA",
        "#E5E7EA"
    ]

    hover_colors = [
        "rgba(0,0,0,0)",
        "#ACACAC",
        "#ACACAC",
        "#ACACAC",
        "#ACACAC",
        "#ACACAC"    
    ]

    sources = [0, 0, 2, 3, 4, 5]            
    targets = [1, 2, 3, 4, 5, 6]

    values = [
        n_not_referred,
        n_intro_to_referred,
        n_referred_to_committee_pass,
        n_committee_to_first_chamber,
        n_first_chamber_to_full,
        n_full_chamber_to_law,
    ]

    percentages = [
        (n_not_referred / n_introduced) * 100,
        (n_intro_to_referred / n_introduced) * 100,
        (n_referred_to_committee_pass / n_intro_to_referred) * 100,
        (n_committee_to_first_chamber / n_referred_to_committee_pass) * 100,
        (n_first_chamber_to_full / n_committee_to_first_chamber) * 100,
        (n_full_chamber_to_law / n_first_chamber_to_full) * 100
    ]

    link_text = [
        "",
        f"{n_intro_to_referred:,} bills passed from<br> {labels[0]} to<br> {labels[2]} ({percentages[1]:.0f}%)",
        f"{n_referred_to_committee_pass:,} bills passed from<br> {labels[2]} to<br> {labels[3]} ({percentages[2]:.0f}%)",
        f"{n_not_referred:,} bills passed from<br> {labels[3]} to<br> {labels[4]} ({percentages[3]:.0f}%)",
        f"{n_intro_to_referred:,} bills passed from<br> {labels[4]} to<br> {labels[5]} ({percentages[4]:.0f}%)",
        f"{n_referred_to_committee_pass:,} bills passed from<br> {labels[5]} to<br> {labels[6]} ({percentages[5]:.0f}%)",
    ]

    node_text= []
    values_all = [n_introduced] + values
    for i, val in enumerate(labels):
        node_text.append(f"{val}<br>{values_all[i]:,} bills<br>{(values_all[i] / n_introduced):.0%} of total")
    node_text[1] = ""

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="fixed",
                node=dict(
                    pad=20,
                    thickness=20,
                    color=node_colors,
                    line=dict(color="white", width=0.5),
                    label=labels,
                    customdata=node_text,
                    hovertemplate="%{customdata}<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="black",
                        font=dict(color="white")
                    )
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                    hovercolor=hover_colors,
                    customdata=link_text,
                    hovertemplate="%{customdata}<extra></extra>",
                    hoverlabel=dict(
                        bgcolor="black",
                        font=dict(color="white")
                    )
                )
            )
        ]
    )   

    fig.update_layout(
        font_size=15,
        width=2000,
        height=600,
    )

    return fig
