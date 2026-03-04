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

MAIN_COLOR = "maroon"
SIZE = 60

def total_donation_history(sponsors):
    df = pd.read_sql(sponsors, db.engine)
    chart = (
        alt.Chart(df)
        .mark_bar(color=MAIN_COLOR)
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
        "names": ["Median", sponsor_name],
        "num_bills": [median_bills, legislator_bills]
    })
    
    chart=(
        alt.Chart(legislator_df)
        .mark_bar(color=MAIN_COLOR)
        .encode(
            x = alt.X("names", title="Legislator", axis=alt.Axis(labelAngle=0)),
            y = alt.Y("num_bills", title="Number of Bills Introduced"))
        .properties(title="Bills Introduced in 102nd & 103rd Sessions",
            width = 300,
            height = 400
        )
    )

    return chart

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
                    range=["#062F8E", "#7C7C7C"]
                    ),
                legend=alt.Legend(
                    titleFontSize=18,
                    labelFontSize=18
                    )
                ))   
        .properties(title="Bill Passage",
            width = 200,
            height = 250
        )
    )

    pie = base.mark_arc(color=MAIN_COLOR, outerRadius= 100)

    return pie

def average_donation_history(sponsors):
    df = pd.read_sql(sponsors, db.engine)
    chart = (
        alt.Chart(df)
        .mark_bar(color=MAIN_COLOR)
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
        .mark_circle(size=SIZE, color=MAIN_COLOR)
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
