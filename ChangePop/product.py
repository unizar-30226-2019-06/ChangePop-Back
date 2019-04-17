import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException
from ChangePop.models import Products, Categories, CatProducts, Images, Bids
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

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/product/<int:id>', methods=['GET'])
def get_prod_info(id):

    product = Products.query.get(int(id))

    if product is None:
        raise ProductException(str(id), "Product not found")

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

    return Response(json.dumps(product_json), status=200, content_type='application/json')


@bp.route('/product/<int:id>', methods=['PUT'])
@login_required
def update_prod_info(id):

    if not request.is_json:
        raise JSONExceptionHandler()

    product = Products.query.get(int(id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    if product.user_id != current_user.id:
        raise UserNotPermission(str(current_user.id), "This user doesnt own this product" + str(id))

    content = request.get_json()

    title = content["title"]
    price = float(content["price"])
    descript = content["descript"]
    bid = datetime.datetime.strptime(content["bid_date"], "%Y-%m-%d %H:%M:%S")
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

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/product/<int:id>', methods=['DELETE'])
@login_required
def delete_product(id):
    # TODO doc
    product = Products.query.get(int(id))

    if product is None:
        raise ProductException(str(id), "Product not found")

    if product.user_id != current_user.id:
        raise UserNotPermission(str(current_user.id), "This user doesnt own this product" + str(id))

    Products.query.get(int(id)).delete_me()
    resp = api_resp(0, "info", "Product: " + str(id) + " deleted")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/products', methods=['GET'])
def list_products():
    # TODO doc
    products = Products.list()

    products_list = []

    for prod in products:

        categories = CatProducts.get_cat_names_by_prod(prod.id)
        cats = []
        for cat in categories:
            cats.append(str(cat))

        item = {
            "id": int(prod.id),
            "descript": str(prod.descript),
            "user_id": int(prod.user_id),
            "price": float(prod.price),
            "title": str(prod.title),
            "categories": cats,
            "bid_date": str(prod.bid_date),
            "boost_date": str(prod.boost_date),
            "followers": int(prod.followers),
            "publish_date": str(prod.publish_date),
            "main_img": str(prod.main_img),
            "place": str(prod.place)
        }

        products_list.append(item)

    json_products = {"length": len(products_list), "list": products_list}

    return Response(json.dumps(json_products), status=200, content_type='application/json')


@bp.route('/products/<int:id>', methods=['GET'])
def list_products_user(id):
    # TODO doc
    products = Products.list_by_id(id)

    products_list = []

    for prod in products:

        categories = CatProducts.get_cat_names_by_prod(prod.id)
        cats = []
        for cat in categories:
            cats.append(str(cat))

        item = {
            "id": int(prod.id),
            "descript": str(prod.descript),
            "user_id": int(prod.user_id),
            "price": float(prod.price),
            "title": str(prod.title),
            "categories": cats,
            "bid_date": str(prod.bid_date),
            "boost_date": str(prod.boost_date),
            "followers": int(prod.followers),
            "publish_date": str(prod.publish_date),
            "main_img": str(prod.main_img),
            "place": str(prod.place)
        }

        products_list.append(item)

    json_products = {"length": len(products_list), "list": products_list}

    return Response(json.dumps(json_products), status=200, content_type='application/json')


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
