from flask import render_template, Response, json, send_file, request
from sqlalchemy.exc import IntegrityError, DatabaseError
from werkzeug.exceptions import BadRequest

from ChangePop import app, user, product, bids, trade, commsg, notify, uploads, reports, payment, category
from ChangePop.exeptions import JSONExceptionHandler, UserException, NotLoggedIn, UserBanned, ProductException
from ChangePop.utils import send_mail

app.register_blueprint(user.bp)
app.register_blueprint(product.bp)
app.register_blueprint(bids.bp)
app.register_blueprint(trade.bp)
app.register_blueprint(commsg.bp)
app.register_blueprint(notify.bp)
app.register_blueprint(uploads.bp)
app.register_blueprint(reports.bp)
app.register_blueprint(category.bp)
app.register_blueprint(payment.bp)


@app.route('/')
def show():
    return render_template('index.html')


@app.route('/test_request') # pragma: no cover
def show_test():
    return render_template('test.html')


@app.route('/test_login') # pragma: no cover
def show_test_login():
    return render_template('test_login.html')


@app.route('/test_mail') # pragma: no cover
def test_mail():
    mail = request.args.get('mail')
    subject = "Test"
    text = "Dear passenger 1, welcome to Mailjet! May the delivery force be with you!"
    html = "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!"
    send_mail(mail, mail, subject, text, html)
    return "Desactivado, ya no va porque nos hakean xD"


@app.route('/<path:dirr>') # pragma: no cover
def file_for_mailjet(dirr):
    return send_file('static/' + dirr)


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


@app.errorhandler(Exception)
def handle_sql_error(error):
    resp = {
        "code": "99",
        "type": "error",
        "message": "Error without concrete exception: " + str(error)}

    return Response(json.dumps(resp), status=400, content_type='application/json')

#TODO Capturar expecion ValueError: time data '25-12-1999' does not match format '%Y-%m-%d'
