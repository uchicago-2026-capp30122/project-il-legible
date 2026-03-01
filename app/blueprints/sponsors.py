from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.database.db import db_session as db
from app.models import Sponsor
from sqlalchemy import select

bp = Blueprint('sponsors', __name__)


@bp.route('/sponsors')
def list_sponsors():
    sponsors = db.scalars(select(Sponsor))
    return render_template('sponsors.html', sponsors=sponsors)
