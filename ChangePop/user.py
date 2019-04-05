import datetime
from typing import Optional, Any

from flask import Blueprint, request, json

bp = Blueprint('user', __name__)

"""
si lo quereis porbar poned este codigo en consola de linux o git:

curl -X POST "http://127.0.0.1:5000/user" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"id\": 0,  \"nick\": \"string\",  \"first_name\": \"string\",  \"last_name\": \"string\",  \"mail\": \"string\",  \"pass_hash\": \"string\",  \"phone\": 0,  \"is_mod\": true,  \"ban_reason\": \"string\",  \"points\": 0,  \"avatar\": \"string\",  \"fnac\": \"2019-04-05\",  \"dni\": 0,  \"place\": \"string\"}"
"""


@bp.route('/user', methods=['POST'])
def create_user():
    content = request.get_json()
    print(content)
    if request.is_json:
        nick = content["nick"]
        first_name = content["first_name"]
        last_name = content["mail"]
        pass_hash = content["pass_hash"]
        phone = int(content["phone"])
        fnac = datetime.datetime.strptime( content["fnac"], "%Y-%m-%d" )
        dni = int(content["dni"])
        place = content["place"]

        print("Creating this following user:\nNick: " + nick + "\nPhone: " + nick + "\nBirth: " + str(fnac.strftime("%x")))

        resp = {
            "code": "0",
            "type": "info",
            "message": "ID DEL NUEVO USUARIO"}

    else:
        resp = {
            "code": "1",
            "type": "error",
            "message": "No JSON found"}

    return json.dumps(resp)



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


