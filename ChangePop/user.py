from typing import Optional, Any

from flask import Blueprint, request

bp = Blueprint('user', __name__)


@bp.route('/user')
def create_user():
    print(request.is_json)
    content = request.get_json()
    print(content)
    print (request.headers)
    return str(request.headers)


@bp.route('/user/<int:id>')
def get_info(id):
    """This function does something.

    :param id: The user identifier
    :type id: str.
    :returns:  str -- JSON of user info.
    :raises: AttributeError, KeyError

    """

    # TODO
    return 'Devolver datos en JSON del usuario' + str (id)


