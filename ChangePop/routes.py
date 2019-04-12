from flask import render_template, Response, json
from werkzeug.exceptions import BadRequest

from ChangePop import models, db, app, user, product
from ChangePop.exeptions import JSONExceptionHandler

app.register_blueprint(user.bp)
app.register_blueprint(product.bp)

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

    return Response(json.dumps(resp), status=400, mimetype='application/json')


@app.errorhandler(JSONExceptionHandler)
def handle_json_error(error):
    resp = {
        "code": "6",
        "type": "error",
        "message": str(error.to_dict())}

    return Response(json.dumps(resp), status=400, mimetype='application/json')
