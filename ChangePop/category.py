import datetime

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Bids, Comments, Users, Trades, Messages, Categories
from ChangePop.utils import api_resp

bp = Blueprint('notify', __name__)


@bp.route('/category', methods=['POST'])
@login_required
def new_category():

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    cat = str(content["cat_name"])

    Categories.add_cat(cat)

    resp = api_resp(0, "info", "Category pushed")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/categories', methods=['GET'])
@login_required
def get_categories():

    notifications = Categories.list_by_user(current_user.id)

    notifications_list = []

    for noti in notifications:

        product_id = str(noti.product_id) if noti.product_id is not None else "null"
        category = str(noti.category) if noti.category is not None else "null"

        item = {
            "id": str(noti.id),
            "user_id": str(noti.user_id),
            "product_id": str(product_id),
            "category": str(category),
            "date": str(noti.date),
            "text": str(noti.text)
        }

        notifications_list.append(item)

    json_notifications = {"length": len(notifications_list), "list": notifications_list}

    return Response(json.dumps(json_notifications), status=200, content_type='application/json')


@bp.route('/categories', methods=['DELETE'])
@login_required
def delete_categories():

    Notifications.delete_all(current_user.id)

    resp = api_resp(0, "info", "Successful delete")

    return Response(json.dumps(resp), status=200, content_type='application/json')

