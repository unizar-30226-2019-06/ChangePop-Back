import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import current_user, login_user, logout_user, login_required
from ChangePop.models import Users

bp = Blueprint('user', __name__)

"""
si lo quereis porbar poned este codigo en consola de linux o git:

curl -X POST "http://127.0.0.1:5000/user" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"id\": 0,  \"nick\": \"string\",  \"first_name\": \"string\",  \"last_name\": \"string\",  \"mail\": \"string\",  \"pass_hash\": \"string\",  \"phone\": 0,  \"is_mod\": true,  \"ban_reason\": \"string\",  \"points\": 0,  \"avatar\": \"string\",  \"fnac\": \"2019-04-05\",  \"dni\": 0,  \"place\": \"string\"}"
"""


@bp.route('/user', methods=['POST'])
def create_user():
    content = request.get_json()
    if request.is_json:
        nick: str = content["nick"]
        first_name = content["first_name"]
        last_name = content["mail"]
        pass_hash = content["pass_hash"]
        phone = int(content["phone"])
        fnac = datetime.datetime.strptime(content["fnac"], "%Y-%m-%d")
        dni = int(content["dni"])
        place = content["place"]
        mail = content["place"]

        user_id = Users.new_user(nick, last_name, first_name, phone, dni, place, pass_hash, fnac, mail)

        # print("Creating this following user:\nId: " + str(user_id) + "\nNick: " + nick + "\nPhone: " + nick + "\nBirth: " + str(fnac.strftime("%x")))

        resp = {
            "code": "0",
            "type": "info",
            "message": str(user_id)}

    else:
        resp = {
            "code": "1",
            "type": "error",
            "message": "No JSON found"}

    return Response(json.dumps(resp), status=0, mimetype='application/json')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    content = request.get_json()
    if request.is_json:
        nick: str = content["nick"]
        pass_hash = content["pass_hash"]
        # esto si no puede ser booleano pues se hace una comparacion y a correr
        recordar = content["recordar_pass"]
        user = Users.query.filter_by(nick=nick).first()
        if user is None or not user.check_password(pass_hash):
            if user is None:
                resp = {
                    "code": "5",
                    "type": "error",
                    "message": "No user found"}
            else:
                resp = {
                    "code": "6",
                    "type": "error",
                    "message": "Wrong password"}
        else:
            resp = {
                "code": "0",
                "type": "info",
                "message": str(nick)}
            # esto te logea
            login_user(user, recordar);
            # ahora si haces current_user deberia ser el usuario que acaba de loggear
    return Response(json.dumps(resp), status=0, mimetype='application/json')


@login_required
@bp.route('/logout')
def logout():
    # asi se sale y se accede a current user en una misma funcion
    nick = current_user.nick
    logout_user()
    return Response(json.dumps(nick), status=0, mimetype='application/json')


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
    return Response(json.dumps(user_json), status=0, mimetype='application/json')
