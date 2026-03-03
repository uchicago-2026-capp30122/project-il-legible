from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app import db
from app.models import Sponsor, Bill
from sqlalchemy import select

bp = Blueprint('viz', __name__)


def list_sponsors():
    sponsors = db.scalars(select(Sponsor))
    return render_template('sponsors.html', sponsors=sponsors)
