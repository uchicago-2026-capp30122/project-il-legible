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

    sponsor_query = select(Sponsor).order_by(Sponsor.effectiveness_score.desc())
    sponsors = db.session.scalars(sponsor_query).all()

    bill_query = select(Bill)
    bills = db.session.scalars(bill_query).all()

    total_donations = sum(s.total_all for s in sponsors if s.total_all is not None)
    total_count_donations = sum(s.donation_count_all for s in sponsors if s.donation_count_all is not None)

    total_bills = Bill.query.count()
    total_passed = Bill.query.filter(Bill.became_law == True).count()

    summary_stats = {
        "total_bills": total_bills,
        "total_donations": total_donations,
        "bill_passage_rate": total_passed / total_bills,
        "last_three_donations": sum(s.total_L3 for s in sponsors if s.total_L3 is not None),
        "average_donation":  total_donations / total_count_donations
    }

    charts = {
        "total_donation_history": viz.total_donation_history(sponsor_query).configure_view(strokeWidth=0).to_json(),
        "average_donation_history": viz.average_donation_history(sponsor_query).configure_view(strokeWidth=0).to_json(),
        "bills_by_donations": viz.bills_by_donations_scatter(sponsor_query).to_json()
    }
    return render_template('insights/index.html', sponsors=sponsors, summary_stats=summary_stats, charts=charts)

