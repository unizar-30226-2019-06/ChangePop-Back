import datetime

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException
from ChangePop.models import Products, Bids, Comments, Users
from ChangePop.utils import api_resp

bp = Blueprint('commsg', __name__)


@bp.route('/comment/<int:id>', methods=['POST'])
@login_required
def new_comment_user(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    body = content["body"]
    points = int(content["points"])

    Comments.add_comment(id, current_user.id, body)
    user = Users.query.get(id)
    user.point_me(points)

    resp = api_resp(0, "info", "New comment created")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/comments/<int:id>', methods=['GET'])
def get_comments_user(id):

    comments = Comments.list_by_user(id)

    comments_list = []

    for com in comments:

        item = {
            "nick": str(Users.get_nick(com.user_from)),
            "body": str(com.body)
        }

        comments_list.append(item)

    json_comments = {"length": len(comments_list), "list": comments_list}

    return Response(json.dumps(json_comments), status=200, content_type='application/json')

