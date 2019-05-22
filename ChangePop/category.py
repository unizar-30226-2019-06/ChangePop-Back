import datetime

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Bids, Comments, Users, Interests, Messages, Categories
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



@bp.route('/categories/interest', methods=['POST'])
@login_required
def new_interest():

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()
    categories_list = content["list"]
    user=current_user.id

    for cat in categories_list:
        Interests.add_interest(cat,user)

    resp = api_resp(0, "info", "Interest pushed")

    return Response(json.dumps(resp), status=200, content_type='application/json')

@bp.route('/categories/interest', methods=['DELETE'])
@login_required
def delete_interest():

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()
    categories_list = content["list"]
    user=current_user.id

    for cat in categories_list:
        Interests.delete_interest(cat,user)

    resp = api_resp(0, "info", "Successful delete")

    return Response(json.dumps(resp), status=200, content_type='application/json')

@bp.route('/categories/interest', methods=['GET'])
@login_required
def get_interest():

    categories = Interests.interest_byUser(current_user.id)

    categories_list = []

    for cat in categories:

        item = cat.cat_name

        categories_list.append(item)

    json_categories = {"length": len(categories_list), "list": categories_list}

    return Response(json.dumps(json_categories), status=200, content_type='application/json')