import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import current_user, login_user, logout_user, login_required

from ChangePop.exeptions import JSONExceptionHandler, UserException, UserPassException, UserNotPermission, UserBanned
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
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    nick: str = content["nick"]
    first_name = content["first_name"]
    last_name = content["last_name"]
    pass_ = content["pass"]
    phone = int(content["phone"])
    fnac = datetime.datetime.strptime(content["fnac"], "%Y-%m-%d")
    dni = int(content["dni"])
    place = content["place"]
    mail = content["mail"]

    user_id = Users.new_user(nick, last_name, first_name, phone, dni, place, pass_, fnac, mail)

    resp = api_resp(0, "info", user_id)

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/user', methods=['GET'])
@login_required
def get_logged_user():
    # TODO Doc
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


@bp.route('/user', methods=['PUT'])
@login_required
def update_logged_user():
    # TODO Doc
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    nick = content["nick"]
    first_name = content["first_name"]
    last_name = content["last_name"]
    phone = int(content["phone"])
    fnac = datetime.datetime.strptime(content["fnac"], "%Y-%m-%d")
    dni = int(content["dni"])
    place = content["place"]
    mail = content["mail"]
    avatar = content["avatar"]

    user_id = current_user.id
    user = Users.query.get(int(user_id))
    user.update_me(nick, first_name, last_name, phone, fnac, dni, place, mail, avatar)

    resp = api_resp(0, "info", "User: " + str(user_id) + ' (' + nick + ') ' + "updated")

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/user', methods=['DELETE'])
@login_required
def delete_logged_user():
    user_id = current_user.id
    current_user.delete_me()
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

    if user.ban_until is not None:
        ban_date = datetime.datetime.strptime(str(user.ban_until), "%Y-%m-%d")
        if ban_date > datetime.datetime.utcnow():
            raise UserBanned(str(nick), None, user.ban_until, user.ban_reason, None)

    login_user(user, remember=bool(remember))

    resp = api_resp(0, "info", "User: " + str(nick) + " logged")

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    # asi se sale y se accede a current user en una misma funcion
    nick = current_user.nick
    logout_user()
    resp = api_resp(0, "info", "Logged out: " + str(nick))
    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    # TODO doc

    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    user = Users.query.get(int(id))

    user_json = {
        "id": str(user.id),
        "nick": str(user.nick),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mail": str(user.mail),
        "pass_hash": str(user.pass_hash),
        "is_mod": str(user.is_mod),
        "ban_reason": str(user.ban_reason),
        "points": str(user.points),
        "phone": str(user.phone),
        "avatar": str(user.avatar),
        "fnac": str(user.fnac),
        "dni": str(user.dni),
        "place": str(user.place),
        "token": str(user.token)
    }

    return Response(json.dumps(user_json), status=200, mimetype='application/json')


@bp.route('/user/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    # TODO doc

    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    if not request.is_json:
        raise JSONExceptionHandler()

    user = Users.query.get(int(id))

    content = request.get_json()

    nick = content["nick"]
    first_name = content["first_name"]
    last_name = content["mail"]
    phone = int(content["phone"])
    fnac = datetime.datetime.strptime(content["fnac"], "%Y-%m-%d")
    dni = int(content["dni"])
    place = content["place"]
    mail = content["place"]
    avatar = content["avatar"]
    is_mod = content["is_mod"]
    ban_reason = content["ban_reason"]
    token = content["token"]
    points = content["points"]
    pass_hash = content["pass_hash"]

    user.update_me(nick, first_name, last_name, phone, fnac, dni, place, mail, avatar, is_mod, ban_reason,
                   token, points, pass_hash)

    resp = api_resp(0, "info", "User: " + str(id) + ' (' + nick + ') ' + "updated")

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    # TODO doc

    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    Users.query.get(int(id)).delete_me()
    resp = api_resp(0, "info", "User: " + str(id) + " deleted")
    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/profile/<string:nick>', methods=['GET'])
def get_profile(nick):
    # TODO doc

    user = Users.query.filter_by(nick=str(nick)).first()

    user_json = {
        "id": str(user.id),
        "nick": str(user.nick),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mail": str(user.mail),
        "points": str(user.points),
        "phone": str(user.phone),
        "avatar": str(user.avatar),
        "fnac": str(user.fnac),
        "place": str(user.place)
    }

    return Response(json.dumps(user_json), status=200, mimetype='application/json')


@bp.route('/user/<int:id>/ban', methods=['PUT'])
@login_required
def set_ban_user(id):
    # TODO doc
    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    ban_reason = content["ban_reason"]
    ban_until = datetime.datetime.strptime(content["ban_until"], "%Y-%m-%d")

    Users.query.get(int(id)).ban_me(ban_reason,ban_until)
    resp = api_resp(0, "info", "User" + ' (' + str(id) + ') ' + "banned")

    return Response(json.dumps(resp), status=200, mimetype='application/json')


# TODO: Esta accesible para todos por motivos de depuración
@bp.route('/user/<int:id>/mod', methods=['PUT'])
def set_mod_user(id):
    # TODO doc

    Users.query.get(int(id)).mod_me()
    resp = api_resp(0, "info", "All Ok")

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/users', methods=['GET'])
def list_users():
    # TODO doc y mas cosas

    users = Users.list_users()
    json_users = []

    for user in users:
        item = {"nick": user.nick,
                "id": user.id,
                "mail": user.mail
                }

        json_users.append(item)

    return Response(json.dumps(json_users), status=200, mimetype='application/json')

