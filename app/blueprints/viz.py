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
        .properties(title=f"Total Donation Amounts of Primary Sponsors in 102nd & 103rd Sessions")
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



