from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Bill
from sqlalchemy import select

bp = Blueprint('bills', __name__)


@bp.route('/bills')
def index():
    query = select(Bill)
    bills = db.session.scalars(query).all()
    return render_template('bills/index.html', bills = bills)


@bp.route("/bills/<int:bill_id>")
def show(bill_id):
    query = select(Bill).filter(Bill.id == bill_id)
    bill = db.session.scalar(query)
    return render_template('bills/show.html', bill=bill)