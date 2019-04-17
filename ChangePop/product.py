import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission
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


@bp.route('/product/<int:id>', methods=['GET'])
def get_prod_info(id):

    product = Products.query.get(int(id))

    categories = CatProducts.get_cat_names_by_prod(id)
    cats = []
    for cat in categories:
        cats.append(str(cat))

    images = Images.get_images_by_prod(id)
    imgs = []
    for img in images:
        imgs.append(str(img))

    product_json = {

        "id": int(product.id),
        "descript": str(product.descript),
        "user_id": int(product.user_id),
        "price": float(product.price),
        "categories": cats,
        "title": str(product.title),
        "bid_date": str(product.bid_date),
        "boost_date": str(product.id),
        "visits": int(product.visits),
        "followers": int(product.followers),
        "publish_date": str(product.publish_date),
        "main_img": str(product.main_img),
        "photo_urls": imgs,
        "place": str(product.place),
        "ban_reason": str(product.ban_reason)

    }

    return Response(json.dumps(product_json), status=200, mimetype='application/json')


@bp.route('/product/<int:id>', methods=['PUT'])
@login_required
def update_prod_info(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    product = Products.query.get(int(id))

    if product.user_id != current_user.id:
        raise UserNotPermission(str(current_user.id), "This user doesnt own this product" + str(id))

    content = request.get_json()

    title = content["title"]
    price = float(content["price"])
    descript = content["descript"]
    bid = datetime.datetime.strptime(content["bid_date"], "%Y-%m-%d")
    categories = content["categories"]
    photo_urls = content["photo_urls"]
    place = content["place"]
    main_img = content["main_img"]

    CatProducts.delete_cats_by_prod(id)
    Images.delete_images_by_prod(id)

    for cat in categories:
        Categories.add_cat(cat)
        CatProducts.add_prod(cat, id)

    for photo in photo_urls:
        Images.add_photo(photo, id)

    product.update_me(title, price, descript, bid, place, main_img)

    resp = api_resp(0, "info", "Product: " + str(id) + ' (' + title + ') ' + "updated")

    return Response(json.dumps(resp), status=200, mimetype='application/json')
