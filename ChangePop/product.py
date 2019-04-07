import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from ChangePop.models import Products, Categories, CatProducts, Images

bp = Blueprint('product', __name__)

"""
si lo quereis porbar poned este codigo en consola de linux o git:

curl -X POST "http://127.0.0.1:5000/product" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"id\": 0,  \"descript\": \"This product is wonderful\",  \"user_id\": 1,  \"price\": 0,  \"categories\": [    \"Moda\", \"Gafas\"  ],  \"title\": \"Producto Molongo\",  \"bid\": \"2019-04-07\",  \"boost_date\": \"2019-04-07\",  \"visits\": 0,  \"followers\": 0,  \"publish_date\": \"2019-04-07\",  \"photo_urls\": [    \"http://images.com/123af3\"  ],  \"place\": \"Zaragoza\",  \"is_removed\": true,  \"ban_reason\": \"Razon Baneo\"}"

"""


@bp.route('/product', methods=['POST'])
def create_product():
    content = request.get_json()
    print(content)
    if request.is_json:

        title = content["title"]
        price = float(content["price"])
        user_id = int(content["user_id"])
        descript = content["descript"]
        categories = content["categories"]
        photo_urls = content["photo_urls"]
        place = content["place"]

        product_id = Products.new_product(user_id, title, descript, price, place)
        print("Created this product:\nId: " + str(product_id) + "\nTitle: " + title)

        for cat in categories:
            Categories.add_cat(cat)
            CatProducts.add_prod(cat, product_id)

        for photo in photo_urls:
            Images.add_photo(photo, product_id)

        resp = {
            "code": "0",
            "type": "info",
            "message": str(product_id)}

    else:
        resp = {
            "code": "1",
            "type": "error",
            "message": "No JSON found"}

    return Response(json.dumps(resp), status=0, mimetype='application/json')


@bp.route('/product/<int:id>')
def get_info(id):
    """This function does something.

    :param id: The user identifier
    :type id: str.
    :returns:  str -- JSON of user info.
    :raises: AttributeError, KeyError

    """

    user = models.Users.query.get(id).first()

    user_json = {
        "id": str(user.id),
        "nick": str(user.nick),
        "first_name": str(user.first_name),
        "last_name": str(user.last_name),
        "mail": str(user.mail),
        "pass_hash": str(user.pass_hash),
        "phone": str(user.phone),
        "avatar": str(user.avatar),
        "fnac": str(user.fnac),
        "dni": str(user.dni),
        "place": str(user.place)
    }

    # TODO
    return Response(json.dumps(user_json), status=0, mimetype='application/json')
