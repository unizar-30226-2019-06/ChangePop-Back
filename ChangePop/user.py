import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import current_user, login_user, logout_user, login_required

from ChangePop.exeptions import JSONExceptionHandler, UserException, UserPassException
from ChangePop.models import Users
from ChangePop.utils import api_resp

bp = Blueprint('user', __name__)

"""
si lo quereis porbar poned este codigo en consola de linux o git:

curl -X POST "http://127.0.0.1:5000/user" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"id\": 0,  \"nick\": \"string\",  \"first_name\": \"string\",  \"last_name\": \"string\",  \"mail\": \"string\",  \"pass_hash\": \"string\",  \"phone\": 0,  \"is_mod\": true,  \"ban_reason\": \"string\",  \"points\": 0,  \"avatar\": \"string\",  \"fnac\": \"2019-04-05\",  \"dni\": 0,  \"place\": \"string\"}"
"""


@bp.route('/user', methods=['POST'])
def create_user():
    """ Add user to the database getting the info from the
    json of the request

        :returns: api response with the id of the new user
        :raises: KeyError, JSONExceptionHandler

        """
    content = request.get_json()

    if not request.is_json:
        raise JSONExceptionHandler()

    nick: str = content["nick"]
    first_name = content["first_name"]
    last_name = content["mail"]
    pass_ = content["pass"]
    phone = int(content["phone"])
    fnac = datetime.datetime.strptime(content["fnac"], "%Y-%m-%d")
    dni = int(content["dni"])
    place = content["place"]
    mail = content["place"]

    user_id = Users.new_user(nick, last_name, first_name, phone, dni, place, pass_, fnac, mail)

    resp = api_resp(0, "info", user_id)

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/user', methods=['GET'])
@login_required
def get_logged_user():
    user_id = current_user.id

    user = Users.query.get(int(user_id))

    user_json = {
        "id": str(user.id),
        "nick": str(user.nick),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mail": str(user.mail),
        "pass_hash": str(user.pass_hash),
        "phone": str(user.phone),
        "avatar": str(user.avatar),
        "fnac": str(user.fnac),
        "dni": str(user.dni),
        "place": str(user.place),
        "is_mod": str(user.is_mod),
        "token": str(user.token),
        "ban_reason": str(user.ban_reason),
        "points": str(user.points)
    }

    return Response(json.dumps(user_json), status=200, mimetype='application/json')


@bp.route('/user', methods=['DELETE'])
@login_required
def delete_logged_user():
    user_id = current_user.id
    Users.delete_user(user_id)
    resp = api_resp(0, "info", "User: " + str(user_id) + " deleted")
    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()
    nick = content["nick"]
    pass_ = content["pass"]
    remember = content["remember"]

    user = Users.query.filter_by(nick=nick).first()

    if user is None:
        raise UserException(str(nick))

    if not user.check_password(pass_):
        raise UserPassException(str(nick))

    login_user(user, remember=bool(remember))

    resp = api_resp(0, "info", "User: " + str(nick) + " logged")

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/logout')
@login_required
def logout():
    # asi se sale y se accede a current user en una misma funcion
    nick = current_user.nick
    logout_user()
    return Response(json.dumps(nick), status=200, mimetype='application/json')


@bp.route('/user/<int:id>')
def get_info(id):
    """This function does something.

    :param id: The user identifier
    :type id: str.
    :returns:  str -- JSON of user info.
    :raises: AttributeError, KeyError

    """

    user = Users.query.get(int(id))

    user_json = {
        "id": str(user.id),
        "nick": str(user.nick),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mail": str(user.mail),
        "pass_hash": str(user.pass_hash),
        "phone": str(user.phone),
        "avatar": str(user.avatar),
        "fnac": str(user.fnac),
        "dni": str(user.dni),
        "place": str(user.place)
    }

    # TODO: More Attributes
    return Response(json.dumps(user_json), status=200, mimetype='application/json')
