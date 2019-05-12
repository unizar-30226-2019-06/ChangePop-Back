import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Categories, CatProducts, Images, Bids, Users, Trades, TradesOffers, Payments
from ChangePop.utils import api_resp

bp = Blueprint('payment', __name__)


@bp.route('/payment', methods=['POST'])
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

    trade_id = Payments.add(product_id, seller_id, buyer_id)

    resp = api_resp(0, "info", str(trade_id))

    return Response(json.dumps(resp), status=200, content_type='application/json')




@bp.route('/payment/<int:id>/close', methods=['PUT'])
@login_required
def payment_close(id):
    trade = Payments.query.get(int(id))

    if trade is None:
        raise TradeException(str(id))

    # TODO Cambiar requisito para k sea mas normal esto?
    # if trade.user_sell != current_user.id and trade.user_buy != current_user.id:
    if trade.user_sell != current_user.id:
        raise UserNotPermission(str(id), "Tis user (" + str(current_user.nick) + ") is not related with this trade")

    trade.closed_b = True
    trade.closed_s = True

    resp = api_resp(0, "info", "Success close for trade " + '(' + str(id) + ')')

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/payment', methods=['GET'])
@login_required
def get_list_payments():

    trades = Payments.get_trades(current_user.id)

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
            "price": float(t.price),
            "last_edit": str(t.ts_edit)
        }

        trades_list.append(str(t_json))

    json_trades = {"length": len(trades_list), "list": trades_list}

    return Response(json.dumps(json_trades), status=200, content_type='application/json')