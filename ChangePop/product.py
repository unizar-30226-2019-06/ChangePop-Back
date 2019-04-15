import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler
from ChangePop.models import Products, Categories, CatProducts, Images
from ChangePop.utils import api_resp

bp = Blueprint('product', __name__)


@bp.route('/product', methods=['POST'])
@login_required
def create_product():

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    title = content["title"]
    price = float(content["price"])
    user_id = str(current_user.id)
    descript = content["descript"]
    categories = content["categories"]
    photo_urls = content["photo_urls"]
    place = content["place"]
    main_img = content["main_img"]

    product_id = Products.new_product(user_id, title, descript, price, place, main_img)

    for cat in categories:
        Categories.add_cat(cat)
        CatProducts.add_prod(cat, product_id)

    for photo in photo_urls:
        Images.add_photo(photo, product_id)

    resp = api_resp(0, "info", str(product_id))

    return Response(json.dumps(resp), status=200, mimetype='application/json')


@bp.route('/product/<int:id>')
def get_info(id):
    """This function does something.

    :param id: The user identifier
    :type id: str.
    :returns:  str -- JSON of user info.
    :raises: AttributeError, KeyError

    """

    product = Products.query.get(int(id))

    # TODO: More Attributes
    product_json = {
        "id": str(product.id),
        "place": str(product.place)
    }

    return Response(json.dumps(product_json), status=200, mimetype='application/json')
