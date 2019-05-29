import datetime

from flask import Blueprint, request, json, Response
from flask_cors import CORS
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException, UserException
from ChangePop.models import Products, Bids, Comments, Users, Trades, Messages
from ChangePop.utils import api_resp

bp = Blueprint('commsg', __name__)

CORS(bp)


@bp.route('/comment/<int:id>', methods=['POST'])
@login_required
def new_comment_user(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    body = content["body"]
    points = int(content["points"])

    cmmnt_id = Comments.add_comment(id, current_user.id, body)
    user = Users.query.get(id)
    user.point_me(points)

    resp = api_resp(0, "info", str(cmmnt_id))

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/comment/<int:id>/del', methods=['DELETE'])
@login_required
def delete_comment_user(id):

    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    if Comments.query.get(id) is None:
        raise UserException(str(id), "Comment not found")

    Comments.delete_comment(id)

    resp = api_resp(0, "info", "Comment (" + str(id) + ")deleted")

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


@bp.route('/msgs/<int:trade_id>', methods=['POST'])
@login_required
def new_message(trade_id):

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    text = content["body"]

    trade = Trades.query.get(trade_id)

    if trade is None:
        raise TradeException(trade_id, "This trade isnt exist")

    user_from = current_user.id

    if trade.user_sell == user_from:
        user_to = trade.user_buy
    elif trade.user_buy == user_from:
        user_to = trade.user_sell
    else:
        raise TradeException(trade_id, "This user inst related with this trade")

    Messages.new_msg(trade_id, user_to, user_from, text)

    resp = api_resp(0, "info", "Message created")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/msgs/<int:trade_id>', methods=['GET'])
@login_required
def get_messages(trade_id):

    trade = Trades.query.get(trade_id)

    if trade is None:
        raise TradeException(trade_id, "This trade isnt exist")

    user = current_user.id

    if trade.user_sell != user and trade.user_buy != user:
        raise TradeException(trade_id, "This user inst related with this trade")

    messages = Messages.get_msgs(trade_id)

    messages_list = []

    for msg in messages:
        item = {
            "nick": str(Users.get_nick(msg.user_from)),
            "date": str(msg.msg_date),
            "body": str(msg.body)
        }

        messages_list.append(item)

    json_messages = {"length": len(messages_list), "list": messages_list}

    return Response(json.dumps(json_messages), status=200, content_type='application/json')
