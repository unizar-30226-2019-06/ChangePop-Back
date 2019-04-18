import datetime

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException
from ChangePop.models import Products, Bids
from ChangePop.utils import api_resp

bp = Blueprint('bids', __name__)


@bp.route('/product/<int:id>/bidup', methods=['PUT'])
@login_required
def bid_up_prod(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    product = Products.query.get(int(id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    if product.user_id != current_user.id:
        raise UserNotPermission(str(current_user.id), "This user doesnt own this product" + str(id))

    content = request.get_json()

    bid = datetime.datetime.strptime(content["bid_until"], "%Y-%m-%d %H:%M:%S")

    product.bid_set(bid)

    resp = api_resp(0, "info", "Product: " + str(id) + ' (' + str(product.title) + ') ' +
                    "set bid for " + bid.strftime("%Y-%m-%d %H:%M:%S"))

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/product/<int:id>/biddown', methods=['PUT'])
@login_required
def bid_down_prod(id):

    product = Products.query.get(int(id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    if product.user_id != current_user.id:
        raise UserNotPermission(str(current_user.id), "This user doesnt own this product" + str(id))

    bid = None

    product.bid_set(bid)

    resp = api_resp(0, "info", "Product: " + str(id) + ' (' + str(product.title) + ') ' +
                    "bid finished")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/bid/<int:id>', methods=['GET'])
def get_bid(id):
    # TODO doc

    bid = Products.query.get(id)

    if bid is None:
        raise ProductException(str(id), "Product not found")

    if bid.bid_date is None:
        raise ProductException(str(id), "Product isnt a bid")

    max_bid = Bids.get_max(bid.id)

    if max_bid is None:
        max_bid_bid = 0
        max_bid_user_id = None
    else:
        max_bid_bid = max_bid.bid
        max_bid_user_id = max_bid.user_id

    item = {
        "id": int(bid.id),
        "title": str(bid.title),
        "bid_date": str(bid.bid_date),
        "main_img": str(bid.main_img),
        "max_bid": float(max_bid_bid),
        "max_bid_user": max_bid_user_id
    }

    return Response(json.dumps(item), status=200, content_type='application/json')


@bp.route('/bids', methods=['GET'])
def list_bids():
    # TODO doc
    bids = Products.query.filter(Products.bid_date != None)

    bids_list = []

    for bid in bids:
        max_bid = Bids.get_max(bid.id)

        if max_bid is None:
            max_bid_bid = 0
            max_bid_user_id = None
        else:
            max_bid_bid = max_bid.bid
            max_bid_user_id = max_bid.user_id


        item = {
            "id": int(bid.id),
            "title": str(bid.title),
            "bid_date": str(bid.bid_date),
            "main_img": str(bid.main_img),
            "max_bid": float(max_bid_bid),
            "max_bid_user": max_bid_user_id
        }

        bids_list.append(item)

    json_products = {"length": len(bids_list), "list": bids_list}

    return Response(json.dumps(json_products), status=200, content_type='application/json')
