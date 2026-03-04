from flask import (
    Blueprint
)

from werkzeug.exceptions import abort

bp = Blueprint('template_filters', __name__)


@bp.app_template_filter('currency_format')
def currency_format(value, currency_symbol="$"):
    if(value is None):
        return ""
    value = float(value)
    return f"{currency_symbol}{value:,.2f}"


@bp.app_template_filter('percent_format')
def percent_format(value):
    if(value is None):
        return ""
    value = float(value)
    return f"{value:,.2%}"


@bp.app_template_filter('score_format')
def score_format(value):
    if(value is None):
        return ""
    value = int(value * 100)
    return value


@bp.app_template_filter('number_format')
def number_format(value):
    if(value is None):
        return ""
    value = int(value)
    return f"{value:,}"