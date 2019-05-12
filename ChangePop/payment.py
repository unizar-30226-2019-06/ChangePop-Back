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
def create_payment():
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    amount = content["amount"]
    iban = content["iban"]
    pay_date = datetime.datetime.strptime(content["pay_date"], "%Y-%m-%d")
    boost_date = datetime.datetime.strptime(content["boost_date"], "%Y-%m-%d")
    product_id = int(content["product_id"])

    product = Products.query.get(int(product_id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    payment_id = Payments.add(amount, iban, pay_date, boost_date, product_id)

    resp = api_resp(0, "info", str(payment_id))

    return Response(json.dumps(resp), status=200, content_type='application/json')




@bp.route('/payment/<int:id>/close', methods=['PUT'])
@login_required
def payment_close(id):
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    price = float(content["price"])
    products = content["products"]

    trade = Trades.query.get(int(id))

    if trade is None:
        raise TradeException(str(id))

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