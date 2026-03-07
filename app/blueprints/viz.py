from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor, Bill
from sqlalchemy import select
import pandas as pd
import altair as alt

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
        .mark_bar(color=COLORS["blue"])
        .encode(
            x = alt.X(
                "total_all",
                title="Total Donation Amounts",
                bin=alt.Bin(maxbins=50),
                axis=alt.Axis(
                    tickMinStep=2_000_000,
                    labelExpr="datum.value % 10000000 === 0 ? format(datum.value, '~s') : ''")
                    ),
            y = alt.Y(
                'count()',
                title = "Number of Sponsors",
                axis=alt.Axis(grid=False))
            )
        .properties(title=f"Total Donation Amounts of Primary Sponsors in 102nd & 103rd Sessions", width="container")
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
        .mark_bar(color=COLORS["blue"])
        .encode(
            x = alt.X(
                "avg_donation_all",
                title="Average Donation Amount",
                bin=alt.Bin(maxbins=50),
                axis=alt.Axis(format="~s")
                ),
            y = alt.Y(
                'count()',
                title = "Number of Sponsors",
                axis=alt.Axis(grid=False))
                )
        .properties(title=f"Average Donation Amount of Primary Sponsors in 102nd & 103rd Sessions", width="container")
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

    chart=(
        alt.Chart(df)
        .add_params(donation_choice)
        .transform_calculate(
            donation_x=
            "DonationWindow == 'All time' ? datum.total_all : datum.total_L3"
            )
        .mark_circle(size=SIZE, color=COLORS["blue"])
        .encode(
            x = alt.X("donation_x:Q", title="Total Donation Amount"),
            y = alt.Y("num_bills", title="Number of Bills Introduced"),
            tooltip=[
                alt.Tooltip("name", title="Legislator"),
                alt.Tooltip("total_all", title="All-time Donations"),
                alt.Tooltip("total_L3", title="Last 3 years Donations"),
                alt.Tooltip("num_bills", title="Bills Introduced")
            ],
            href="url:N"
            )
        .interactive()
        .properties(title="Total Donations vs Number of Bills Introduced in 102nd & 103rd Sessions", width="container")
        .transform_calculate(
            url='/sponsors/' + alt.datum.id
        )
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
        .mark_bar(color=COLORS["orange"], size=30)
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
            color=COLORS["orange"]
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
        .mark_bar(color=COLORS["orange"], size=30)
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
            color=COLORS["orange"]
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
        .mark_bar(color=COLORS["orange"], size=30)
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
            color=COLORS["orange"]
        )
        .encode(
            x=pct_selected + ":Q",
            y="category:N",
            text=alt.Text(pct_selected + ":Q", format=".0%")
        )
    )
    
    chart = (bars + labels)
        
    return chart
