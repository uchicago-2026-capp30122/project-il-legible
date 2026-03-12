from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.blueprints import viz
from app.models import Sponsor
from sqlalchemy import select

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    chart = viz.total_donation_history(select(Sponsor))
    return render_template("index.html", chart=chart.to_json())
