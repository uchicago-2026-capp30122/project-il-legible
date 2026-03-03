from flask import (
    Blueprint, jsonify
)
from werkzeug.exceptions import abort
from app import db
from app.models import Bill, Sponsor

bp = Blueprint('api', __name__)


@bp.route('/api/sponsors', methods=['GET'])
def get_sponsors():
    data = {'data': [sponsor.to_dict() for sponsor in Sponsor.query]}
    return jsonify(data), 200


@bp.route('/api/bills', methods=['GET'])
def get_bills():
    data = {'data': [bill.to_dict() for bill in Bill.query]}
    return jsonify(data), 200