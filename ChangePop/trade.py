import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_cors import CORS
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Categories, CatProducts, Images, Bids, Users, Trades, TradesOffers
from ChangePop.utils import api_resp

bp = Blueprint('trade', __name__)

CORS(bp, supports_credentials=True, origins=['https://changepop-fw.herokuapp.com', '127.0.0.1:5000'])


@bp.route('/trade', methods=['POST'])
@login_required
def create_trade():
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    seller_id = content["seller_id"]
    buyer_id = content["buyer_id"]
    product_id = int(content["product_id"])

    product = Products.query.get(int(product_id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    trade_id = Trades.add(product_id, seller_id, buyer_id)

    resp = api_resp(0, "info", str(trade_id))

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/trade/<int:id>', methods=['GET'])
@login_required
def get_trade(id):
    trade = Trades.query.get(int(id))

    if trade is None:
        raise TradeException(str(id))

    if trade.user_sell != current_user.id and trade.user_buy != current_user.id:
        raise UserNotPermission(str(id), "This user (" + str(current_user.nick) + ") is not related with this trade")

    product = Products.query.get(trade.product_id)

    products = TradesOffers.get_prods_by_id(id)
    prods = []
    for p in products:
        prods.append(str(p))

    trade_json = {
        "id": int(id),
        "product_id": int(trade.product_id),
        "product_title": str(product.title),
        "seller_id": int(trade.user_sell),
        "buyer_id": int(trade.user_buy),
        "closed": bool(trade.closed_s and trade.closed_b),
        "closed_s": bool(trade.closed_s),
        "closed_b": bool(trade.closed_b),
        "price": float(trade.price),
        "last_edit": str(trade.ts_edit),
        "products_offer": prods
    }

    return Response(json.dumps(trade_json), status=200, content_type='application/json')


@bp.route('/trade/<int:id>/offer', methods=['POST'])
@login_required
def trade_offer(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    price = float(content["price"])
    products = content["products"]

    trade = Trades.query.get(int(id))

    if trade is None:
        raise TradeException(str(id))

    if trade.closed_s and trade.closed_b:
        raise TradeException(str(id), "The trade is already closed, no chages allowed")

    if trade.closed_s or trade.closed_b:
        raise TradeException(str(id), "The trade is on confirm status")

    if trade.user_sell != current_user.id and trade.user_buy != current_user.id:
        raise UserNotPermission(str(id), "This user (" + str(current_user.nick) + ") is not related with this trade")

    # Set the price

    trade.set_price(price)

    # Add products to the offer

    for p in products:
        TradesOffers.add_product(id, p)

    resp = api_resp(0, "info", "Successful new offer")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/trade/<int:id>/offer', methods=['PUT'])
@login_required
def trade_edit_offer(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    price = float(content["price"])
    products = content["products"]

    trade = Trades.query.get(int(id))

    if trade is None:
        raise TradeException(str(id))

    if trade.closed_s and trade.closed_b:
        raise TradeException(str(id), "The trade is already closed, no chages allowed")

    if trade.user_sell != current_user.id and trade.user_buy != current_user.id:
        raise UserNotPermission(str(id), "This user (" + str(current_user.nick) + ") is not related with this trade")

    # Set the price

    trade.set_price(price)

    # Add products to the offer

    TradesOffers.delete_all(id)
    for p in products:
        TradesOffers.add_product(id, p)

    resp = api_resp(0, "info", "Successful offer update")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/trade/<int:id>/delete', methods=['PUT'])
@login_required
def trade_close(id):
    trade = Trades.query.get(int(id))

    if trade is None:
        raise TradeException(str(id))

    if trade.user_sell != current_user.id:
        raise UserNotPermission(str(id), "Tis user (" + str(current_user.nick) + ") is not related with this trade")

    Trades.delete_id(id)

    resp = api_resp(0, "info", "Success delete of trade " + '(' + str(id) + ')')

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/trade/<int:id>/confirm', methods=['PUT'])
@login_required
def trade_confirm(id):
    trade = Trades.query.get(int(id))

    if trade is None:
        raise TradeException(str(id), "Trade not found")

    if trade.closed_s and trade.closed_b:
        raise TradeException(str(id), "The trade is already closed, no chages allowed")

    if current_user.id == trade.user_sell:
        trade.switch('s')
        if trade.closed_s:
            resp = api_resp(0, "info", "Success confirm for trade " + '(' + str(id) + ')')
        else:
            resp = api_resp(0, "info", "Success unconfirm for trade " + '(' + str(id) + ')')
    elif trade.user_buy == current_user.id:
        trade.switch('b')
        if trade.closed_b:
            resp = api_resp(0, "info", "Success confirm for trade " + '(' + str(id) + ')')
        else:
            resp = api_resp(0, "info", "Success unconfirm for trade " + '(' + str(id) + ')')
    else:
        raise UserNotPermission(str(id), "Tis user (" + str(current_user.nick) + ") is not related with this trade")

    if trade.closed_s and trade.closed_b:
        resp = api_resp(0, "info", "Success confirm and close for trade " + '(' + str(id) + ')')

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/trades', methods=['GET'])
@login_required
def get_list_trades():

    trades = Trades.get_trades(current_user.id)

    trades_list = []
    for t in trades:
        product = Products.query.get(t.product_id)
        t_json = {
            "id": int(t.id),
            "product_id": int(t.product_id),
            "product_title": str(product.title),
            "seller_id": int(t.user_sell),
            "buyer_id": int(t.user_buy),
            "closed": bool(t.closed_s and t.closed_b),
            "closed_s": bool(t.closed_s),
            "closed_b": bool(t.closed_b),
            "price": float(t.price),
            "last_edit": str(t.ts_edit)
        }

        trades_list.append(t_json)

    json_trades = {"length": len(trades_list), "list": trades_list}

    return Response(json.dumps(json_trades), status=200, content_type='application/json')
