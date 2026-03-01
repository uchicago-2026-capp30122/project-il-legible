from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.database.db import db_session as db
from app.models import Bill
from sqlalchemy import select

bp = Blueprint('bills', __name__)


@bp.route('/bills')
def list_sponsors():
    bills = db.scalars(select(Bill))
    return render_template('bills.html', bills = bills)
