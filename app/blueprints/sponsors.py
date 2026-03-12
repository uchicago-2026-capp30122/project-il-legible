from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor
from sqlalchemy import select
from app.blueprints import viz

bp = Blueprint("sponsors", __name__)


@bp.route("/sponsors")
def index():
    query = select(Sponsor)
    sponsors = db.session.scalars(query).all()
    return render_template("sponsors/index.html", sponsors=sponsors)


@bp.route("/sponsors/<int:sponsor_id>")
def show(sponsor_id):
    sponsor_query = select(Sponsor)
    query = select(Sponsor).filter(Sponsor.id == sponsor_id)
    sponsor = db.session.scalar(query)

    charts_bills = {
        "num_bills": viz.num_bills_bar(sponsor.name, sponsor_query)
        .configure_view(strokeWidth=0)
        .to_json(),
        "perc_passing": viz.bill_success_legislator(
            sponsor.name, sponsor_query
        ).to_json(),
    }

    if sponsor.donation_count_all is None:
        return render_template(
            "sponsors/show.html", sponsor=sponsor, charts=charts_bills
        )

    charts_donations = {
        "large_donations_lifetime": viz.large_donation_barchart(
            sponsor.name, sponsor_query, "all"
        )
        .configure_view(strokeWidth=0)
        .to_json(),
        "large_donations_L3": viz.large_donation_barchart(
            sponsor.name, sponsor_query, "L3"
        )
        .configure_view(strokeWidth=0)
        .to_json(),
        "entity_donations_lifetime": viz.entity_donation_barchart(
            sponsor.name, sponsor_query, "all"
        )
        .configure_view(strokeWidth=0)
        .to_json(),
        "entity_donations_L3": viz.entity_donation_barchart(
            sponsor.name, sponsor_query, "L3"
        )
        .configure_view(strokeWidth=0)
        .to_json(),
        "state_donations_lifetime": viz.in_state_donation_barchart(
            sponsor.name, sponsor_query, "all"
        )
        .configure_view(strokeWidth=0)
        .to_json(),
        "state_donations_L3": viz.in_state_donation_barchart(
            sponsor.name, sponsor_query, "L3"
        )
        .configure_view(strokeWidth=0)
        .to_json(),
    }

    return render_template(
        "sponsors/show.html", sponsor=sponsor, charts=charts_bills | charts_donations
    )
