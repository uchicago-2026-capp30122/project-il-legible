from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor
from sqlalchemy import select
from app.blueprints import viz

bp = Blueprint('sponsors', __name__)


@bp.route('/sponsors')
def index():
    query = select(Sponsor)
    sponsors = db.session.scalars(query).all()
    return render_template('sponsors/index.html', sponsors=sponsors)


@bp.route("/sponsors/<int:sponsor_id>")
def show(sponsor_id):
    sponsor_query = select(Sponsor)
    query = select(Sponsor).filter(Sponsor.id == sponsor_id)
    sponsor = db.session.scalar(query)

    charts = {
        "num_bills": viz.num_bills_bar(sponsor.name, sponsor_query).to_json(),
        "perc_passing": viz.bill_success_legislator(sponsor.name, sponsor_query).to_json(),
    }
    return render_template('sponsors/show.html', sponsor = sponsor, charts = charts)

