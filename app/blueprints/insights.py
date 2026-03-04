from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor, Bill
from app.blueprints import viz
from sqlalchemy import select, func

bp = Blueprint('insights', __name__)


@bp.route('/insights')
def index():

    query = select(Sponsor).order_by(Sponsor.effectiveness_score.desc())
    sponsors = db.session.scalars(query).all()


    summary_stats = {
        "total_bills": db.session.scalar(select(func.count()).select_from(Bill)),
        "total_donations": sum(s.total_all for s in sponsors if s.total_all is not None),
        "last_three_donations": sum(s.total_L3 for s in sponsors if s.total_L3 is not None)
    }

    charts = {
        "total_donation_history": viz.total_donation_history(query).to_json(),
        "average_donation_history": viz.average_donation_history(query).to_json(),
        "bills_by_donations": viz.bills_by_donations_scatter(query).to_json()
    }
    return render_template('insights/index.html', sponsors=sponsors, summary_stats=summary_stats, charts=charts)

