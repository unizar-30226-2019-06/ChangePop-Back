from flask import render_template, Response, json
from sqlalchemy.exc import IntegrityError, DatabaseError
from werkzeug.exceptions import BadRequest

from ChangePop import app, user, product, bids
from ChangePop.exeptions import JSONExceptionHandler, UserException, NotLoggedIn, UserBanned, ProductException

app.register_blueprint(user.bp)
app.register_blueprint(product.bp)
app.register_blueprint(bids.bp)


@app.route('/')
def show():
    return render_template('index.html')


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!' + "e", 400


@app.errorhandler(KeyError)
def handle_key_error(error):
    resp = {
        "code": "6",
        "type": "error",
        "message": "JSON Key error: " + str(error) + " not found"}

    return Response(json.dumps(resp), status=400, content_type='application/json')


@app.errorhandler(JSONExceptionHandler)
def handle_json_error(error):
    resp = {
        "code": str(error.code),
        "type": "error",
        "message": str(error.to_dict())}

    return Response(json.dumps(resp), status=error.status_code, content_type='application/json')


@app.errorhandler(UserBanned)
def handle_user_banned(error):
    resp = {
        "code": str(error.code),
        "type": "info",
        "ban_reason": str(error.reason),
        "ban_until": str(error.until_date),
        "message": str(error.to_dict())}

    return Response(json.dumps(resp), status=error.status_code, content_type='application/json')


@app.errorhandler(UserException)
def handle_user_exception(error):
    resp = {
        "code": str(error.code),
        "type": "error",
        "message": str(error.to_dict())}

    return Response(json.dumps(resp), status=error.status_code, content_type='application/json')


@app.errorhandler(ProductException)
def handle_user_exception(error):
    resp = {
        "code": str(error.code),
        "type": "error",
        "message": str(error.to_dict())}

    return Response(json.dumps(resp), status=error.status_code, content_type='application/json')


@app.errorhandler(NotLoggedIn)
def handle_user_not_logged(error):
    resp = {
        "code": str(error.code),
        "type": "error",
        "message": str(error.to_dict())}

    return Response(json.dumps(resp), status=error.status_code, content_type='application/json')


@app.errorhandler(DatabaseError)
def handle_sql_error(error):
    resp = {
        "code": "1",
        "type": "error",
        "message": str(error)}

    return Response(json.dumps(resp), status=400, content_type='application/json')


