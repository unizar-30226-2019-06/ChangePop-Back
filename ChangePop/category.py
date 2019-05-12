import datetime

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Bids, Comments, Users, Trades, Messages, Categories
from ChangePop.utils import api_resp

bp = Blueprint('category', __name__)

'''
@bp.route('/category', methods=['POST'])
@login_required
def new_category():

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    cat = str(content["cat_name"])

    Categories.add_cat(cat)

    resp = api_resp(0, "info", "Category pushed")

    return Response(json.dumps(resp), status=200, content_type='application/json')'''


@bp.route('/categories', methods=['GET'])
@login_required
def get_categories():

    categories = Categories.list()

    categories_list = []

    for cat in categories:

        item = cat.cat_name

        categories_list.append(item)

    json_categories = {"length": len(categories_list), "list": categories_list}

    return Response(json.dumps(json_categories), status=200, content_type='application/json')

'''
@bp.route('/category', methods=['DELETE'])
@login_required
def delete_categories():
    # TODO ESTA MAL
    Categories.delete(current_user.id)

    resp = api_resp(0, "info", "Successful delete")

    return Response(json.dumps(resp), status=200, content_type='application/json')'''

