import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response, render_template
from flask_login import current_user, login_user, logout_user, login_required

from ChangePop.exeptions import JSONExceptionHandler, UserException, UserPassException, UserNotPermission, UserBanned, \
    NotLoggedIn
from ChangePop.models import Users
from ChangePop.utils import api_resp, send_mail, random_string

bp = Blueprint('user', __name__)


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

    token = random_string()
    user_id = Users.new_user(nick, last_name, first_name, phone, dni, place, pass_, fnac, mail, token)

    subject = "Confirma tu cuenta"
    link = request.host_url + 'user/' + str(user_id) + '/validate?token=' + token
    text = "Necesitamos que confirmes tu cuenta para poder iniciar sesión en nuestra aplicación, link:" + link
    html = "<p>Necesitamos que confirmes tu cuenta para poder iniciar sesión en nuestra aplicación</p>" \
           "<h3> Link para confirmar: <a href='" + link + "'>Validar</a>!</h3><br />Comienza a intercambiar!"

    if first_name == 'Foo':
        user = Users.query.get(int(user_id))
        user.validate_me()
    else:
        send_mail(mail, first_name + " " + last_name, subject, text, html)

    resp = api_resp(0, "info", user_id)

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/user/<int:id>/validate', methods=['GET'])
def validate_user(id):
    token = request.args.get('token')

    if token is None:
        raise Exception(str(token), "Token is none")

    user = Users.query.get(int(id))

    if user is None:
        raise UserException(str(id))

    if token != user.token:
        raise UserException(str(token), "Worng Token")

    user.validate_me()
    user.set_token(random_string())

    return render_template('close.html')


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

    return Response(json.dumps(user_json), status=200, content_type='application/json')


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

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/user', methods=['DELETE'])
@login_required
def delete_logged_user():
    user_id = current_user.id

    if current_user.first_name == 'Foo':
        current_user.delete_me()
    else:
        token = random_string()
        current_user.set_token(token)
        subject = "Confirma para eliminar tu cuenta"
        link = request.host_url + 'user/' + str(user_id) + '/delete?token=' + token
        text = "Necesitamos que confirmes para eliminar tu cuenta, link: " + link
        html = "<p>Necesitamos que confirmes para eliminar tu cuenta</p>" \
               "<h3> Link para eliminar: <a href='" + link + "'>Eliminar</a>!</h3><br />Se borraran todos tu datos y " \
                                                              "productos, intercambios y demás objetos asociados"
        send_mail(current_user.mail, current_user.first_name + " " + current_user.last_name, subject, text, html)

    resp = api_resp(0, "info", "User: " + str(user_id) + " ready to deleted (mail)")
    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/user/<int:id>/delete', methods=['GET'])
def validate_delete_user(id):
    token = request.args.get('token')

    if token is None:
        raise Exception(str(token), "Token is none")

    user = Users.query.get(int(id))

    if user is None or not user.is_validated:
        raise UserException(str(id))

    if token != user.token:
        raise UserException(str(token), "Worng Token")

    user.delete_me()

    return render_template('close.html')


@bp.route('/login', methods=['POST'])
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

    if not user.is_validated:
        raise UserException(str(nick), "Mail not validated")

    if not user.check_password(pass_):
        raise UserPassException(str(nick))

    if user.ban_until is not None:
        ban_date = datetime.datetime.strptime(str(user.ban_until), "%Y-%m-%d")
        if ban_date > datetime.datetime.utcnow():
            raise UserBanned(str(nick), None, user.ban_until, user.ban_reason, None)

    login_user(user, remember=bool(remember))

    resp = api_resp(0, "info", "User: " + str(nick) + " logged")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    nick = current_user.nick
    logout_user()
    resp = api_resp(0, "info", "Logged out: " + str(nick))
    return Response(json.dumps(resp), status=200, content_type='application/json')


# TODO: falta test
@bp.route('/user/follows', methods=['GET'])
@login_required
def get_user_follows():

    product_list = current_user.my_follows()

    prod_list = []

    for prod in product_list:
        item = {
              "id": str(prod.id),
              "title": str(prod.title),
              "descript": str(prod.descript),
              "price": str(prod.price),
              "main_img": str(prod.main_img)
            }

        prod_list.append(item)

    json_prods = {"length": len(prod_list), "list": prod_list}

    return Response(json.dumps(json_prods), status=200, content_type='application/json')


@bp.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    # TODO doc

    if not current_user.is_mod and False:
        raise UserNotPermission(str(current_user.nick))

    user = Users.query.get(int(id))

    if user is None:
        raise UserException(str(id), "User not found")

    user_json = {
        "id": str(user.id),
        "nick": str(user.nick),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mail": str(user.mail),
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

    return Response(json.dumps(user_json), status=200, content_type='application/json')


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

    user.update_me(nick, first_name, last_name, phone, fnac, dni, place, mail, avatar, is_mod, ban_reason,
                   token, points, None)

    resp = api_resp(0, "info", "User: " + str(id) + ' (' + nick + ') ' + "updated")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    # TODO doc

    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    Users.query.get(int(id)).delete_me()
    resp = api_resp(0, "info", "User: " + str(id) + " deleted")
    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/profile/<string:nick>', methods=['GET'])
def get_profile(nick):
    # TODO doc

    user = Users.query.filter_by(nick=str(nick)).first()

    if user is None:
        raise UserException(str(nick), "User not found")

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

    return Response(json.dumps(user_json), status=200, content_type='application/json')


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

    return Response(json.dumps(resp), status=200, content_type='application/json')


# TODO: Esta accesible para todos por motivos de depuración
@bp.route('/user/<int:id>/mod', methods=['PUT'])
def set_mod_user(id):
    # TODO doc

    Users.query.get(int(id)).mod_me()

    resp = api_resp(0, "info", "All Ok")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/users', methods=['GET'])
def list_users():
    # TODO doc y mas cosas

    users = Users.list_users()

    users_list = []

    for user in users:
        item = {
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

        users_list.append(item)

    json_users = {"length": len(users_list), "list": users_list}

    return Response(json.dumps(json_users), status=200, content_type='application/json')


@bp.route('/search/users', methods=['GET'])
def search_users():
    # TODO doc y mas cosas

    nick_search = request.args.get('text')

    if nick_search is None:
        raise Exception(str(nick_search))

    users = Users.search(nick_search)

    users_list = []

    for user in users:
        item = {
            "id": str(user.id),
            "nick": str(user.nick)
        }

        users_list.append(item)

    json_users = {"length": len(users_list), "list": users_list}

    return Response(json.dumps(json_users), status=200, content_type='application/json')


