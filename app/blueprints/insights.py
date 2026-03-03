from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor, Bill
from sqlalchemy import select
from app.blueprints import viz

bp = Blueprint('insights', __name__)


@bp.route('/insights')
def index():
    query = select(Sponsor)
    chart = viz.total_donation_history(query)
    return render_template('insights/index.html', chart=chart.to_json())

