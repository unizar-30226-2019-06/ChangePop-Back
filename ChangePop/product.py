import datetime
from typing import Optional, Any

from flask import Blueprint, request, json, Response
from flask_cors import CORS
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException
from ChangePop.models import Products, Categories, CatProducts, Images, Bids, Users, Follows, Interests
from ChangePop.utils import api_resp, fix_str, push_notify

bp = Blueprint('product', __name__)

CORS(bp)


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

    if not isinstance(categories, list):
        raise JSONExceptionHandler("Bad format for categories, need an array")

    if not isinstance(photo_urls, list):
        raise JSONExceptionHandler("Bad format for photo_urls, need an array")

    product_id = Products.new_product(user_id, title, descript, price, place, main_img)

    for cat in categories:
        if len(cat) <= 1:
            raise ProductException(title, "Invalid categorie: " + cat)
        Categories.add_cat(cat)
        CatProducts.add_prod(cat, product_id)

    for photo in photo_urls:
        Images.add_photo(photo, product_id)

    # Notificaciones
    for cat in CatProducts.get_cat_names_by_prod(product_id):
        users_ids = Interests.get_users_interest_cat(cat)
        for user_id in users_ids:
            push_notify(user_id, "Nuevo producto en una categoria que te interesa", int(product_id), cat)

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
        cats.append(fix_str(str(cat)))

    product.increment_views()

    images = Images.get_images_by_prod(id)
    imgs = []
    for img in images:
        imgs.append(fix_str(str(img)))

    product_json = {

        "id": int(product.id),
        "descript": str(product.descript),
        "user_id": int(product.user_id),
        "user_nick": str(Users.get_nick(product.user_id)),
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
        "sold": str(product.is_removed),
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

    if not isinstance(categories, list):
        raise JSONExceptionHandler("Bad format for categories, need an array")

    if not isinstance(photo_urls, list):
        raise JSONExceptionHandler("Bad format for photo_urls, need an array")

    CatProducts.delete_cats_by_prod(id)
    Images.delete_images_by_prod(id)

    for cat in categories:
        if len(cat) <= 1:
            raise ProductException(title, "Invalid categorie: " + cat)
        Categories.add_cat(cat)
        CatProducts.add_prod(cat, id)

    for photo in photo_urls:
        Images.add_photo(photo, id)

    # Notificaiones
    if product.price > price:
        users_ids = Follows.get_users_follow_prod(product.id)
        for user_id in users_ids:
            push_notify(user_id, "El precio del producto ha bajado! :D", int(product.id))
    elif product.price < price:
        users_ids = Follows.get_users_follow_prod(product.id)
        for user_id in users_ids:
            push_notify(user_id, "El precio del producto ha subido :(", int(product.id))

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
            cats.append(fix_str(str(cat)))

        item = {
            "id": int(prod.id),
            "descript": str(prod.descript),
            "user_id": int(prod.user_id),
            "user_nick": str(Users.get_nick(prod.user_id)),
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
            cats.append(fix_str(str(cat)))

        images = Images.get_images_by_prod(id)
        imgs = []
        for img in images:
            imgs.append(fix_str(str(img)))

        item = {
            "id": int(prod.id),
            "descript": str(prod.descript),
            "user_id": int(prod.user_id),
            "user_nick": str(Users.get_nick(prod.user_id)),
            "price": float(prod.price),
            "title": str(prod.title),
            "categories": cats,
            "photo_urls": imgs,
            "bid_date": str(prod.bid_date),
            "boost_date": str(prod.boost_date),
            "visits": int(prod.visits),
            "followers": int(prod.followers),
            "publish_date": str(prod.publish_date),
            "main_img": str(prod.main_img),
            "place": str(prod.place),
            "sold": str(prod.is_removed),
            "ban_reason": str(prod.ban_reason)
        }

        products_list.append(item)

    json_products = {"length": len(products_list), "list": products_list}

    return Response(json.dumps(json_products), status=200, content_type='application/json')


@bp.route('/product/<int:id>/follow', methods=['POST'])
@login_required
def follow_product(id):
    # TODO doc

    current_user.follow_prod(id)

    resp = api_resp(0, "info", "User" + ' (' + str(current_user.nick) + ') ' + "follows a product" + ' (' + str(id) + ') ')

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/product/<int:id>/unfollow', methods=['POST'])
@login_required
def unfollow_product(id):
    # TODO doc

    current_user.unfollow_prod(id)

    resp = api_resp(0, "info", "User" + ' (' + str(current_user.nick) + ') ' + "unfollows a product" + ' (' + str(id) + ') ')

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/product/<int:id>/ban', methods=['PUT'])
@login_required
def set_ban_prod(id):
    # TODO doc
    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    ban_reason = content["ban_reason"]

    Products.query.get(int(id)).ban_me(ban_reason)
    resp = api_resp(0, "info", "Product" + ' (' + str(id) + ') ' + "banned")

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/search/products', methods=['GET'])
def search_products():
    # TODO doc y mas cosas

    title_search = request.args.get('text')

    if title_search is None:
        raise Exception(str(title_search))

    products = Products.search(title_search)
    print(products)

    products_list = []

    for prod in products:
        item = {
            "id": str(prod.id),
            "title": str(prod.title),
            "price": float(prod.price),
            "user_nick": str(Users.get_nick(prod.user_id)),
            "visits": int(prod.visits)
        }

        products_list.append(item)

    json_users = {"length": len(products_list), "list": products_list}

    return Response(json.dumps(json_users), status=200, content_type='application/json')


@bp.route('/search/products/adv', methods=['GET'])
def search_products_advanced():
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    title = content["title"]
    price_min = float(content["price_min"])
    price_max = float(content["price_max"])
    place = str(content["place"])
    desc = str(content["descript"])
    category = str(content["category"])

    products = Products.search_adv(title, price_min, price_max, place, desc, category)

    products_list = []

    for prod in products:
        item = {
            "id": str(prod.id),
            "title": str(prod.title),
            "price": float(prod.price),
            "user_nick": str(Users.get_nick(prod.user_id)),
            "visits": int(prod.visits)
        }

        products_list.append(item)

    json_users = {"length": len(products_list), "list": products_list}

    return Response(json.dumps(json_users), status=200, content_type='application/json')
