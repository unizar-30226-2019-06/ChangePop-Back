from flask import Blueprint

bp = Blueprint('user', __name__)


@bp.route('/user/<int:id>')
def get_info(id):
    """This function does something.

    :param id: The user identifier
    :type id: str.
    :returns:  str -- JSON of user info.
    :raises: AttributeError, KeyError

    """

    # TODO
    return 'Devolver datos en JSON del usuario' + id


