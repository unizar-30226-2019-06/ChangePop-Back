from flask import Blueprint, url_for

bp = Blueprint('otro', __name__)


@bp.route('/otro')
def index():
    return 'otro!' + url_for('otro.index')
