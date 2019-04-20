import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Categories, CatProducts, Images, Bids, Users, Trades
from ChangePop.utils import api_resp

bp = Blueprint('trade', __name__)


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
        raise UserNotPermission(str(id), "Tis user (" + str(current_user.nick) + ") is not related with this trade")

    product = Products.query.get(trade.product_id)

    trade_json = {
        "id": int(id),
        "product_id": int(trade.product_id),
        "product_title": str(product.title),
        "seller_id": int(trade.user_sell),
        "buyer_id": int(trade.user_buy),
        "closed": bool(trade.closed_s and trade.closed_b),
        "price": float(trade.price),
        "last_edit": str(trade.ts_edit)
    }

    return Response(json.dumps(trade_json), status=200, content_type='application/json')


@bp.route('/trade/<int:id>/offer', methods=['POST'])
@login_required
def trade_offer(id):
    return ""


@bp.route('/trade/<int:id>/offer', methods=['PUT'])
@login_required
def trade_edit_offer(id):
    return ""


@bp.route('/trade/<int:id>/close', methods=['PUT'])
@login_required
def trade_close(id):
    return ""


@bp.route('/trades', methods=['GET'])
@login_required
def get_list_trades():
    return ""
