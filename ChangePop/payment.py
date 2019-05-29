import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Categories, CatProducts, Images, Bids, Users, Trades, TradesOffers, Payments
from ChangePop.utils import api_resp

bp = Blueprint('payment', __name__)

CORS(bp)


@bp.route('/payment', methods=['POST'])
@login_required
def create_payment():
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    amount = content["amount"]
    iban = content["iban"]
    boost_date = datetime.datetime.strptime(content["boost_date"], "%Y-%m-%d")
    product_id = int(content["product_id"])

    product = Products.query.get(int(product_id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    payment_id = Payments.add(amount, iban, product_id, boost_date)

    resp = api_resp(0, "info", str(payment_id))

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/payment/check/<int:id>', methods=['PUT'])
@login_required
def payment_check(id):
    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    pay = Payments.query.get(int(id))

    if pay is None:
        raise ProductException(str(id), "Payment of product not found")

    Payments.query.get(int(id)).delete_me()
    resp = api_resp(0, "info", "Payment: " + str(id) + " deleted")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/payments', methods=['GET'])
@login_required
def get_list_payments():
    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    payments = Payments.list()

    payments_list = []

    for pay in payments:

        item = {
            "id": int(pay.id),
            "pay_date": str(pay.pay_date),
            "amount": float(pay.amount),
            "iban": str(pay.iban),
            "boost_date": str(pay.boost_date),
            "product_id": int(pay.product_id),
        }

        payments_list.append(item)

    json_products = {"length": len(payments_list), "list": payments_list}

    return Response(json.dumps(json_products), status=200, content_type='application/json')
