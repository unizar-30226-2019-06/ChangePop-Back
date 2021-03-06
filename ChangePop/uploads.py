import datetime
import os
import random
import string

from flask import Blueprint, request, json, Response, send_from_directory, send_file
from flask_cors import CORS
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ChangePop import app, ALLOWED_EXTENSIONS
from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException, TradeException
from ChangePop.models import Products, Bids, Comments, Users, Trades, Messages, Notifications
from ChangePop.utils import api_resp, random_string

bp = Blueprint('uploads', __name__)

CORS(bp, supports_credentials=True, origins=['https://changepop-fw.herokuapp.com', '127.0.0.1:5000'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():

    # check if the post request has the file part
    if 'file' not in request.files:
        raise Exception('No file part')

    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        raise Exception('No selected file')

    if file and allowed_file(file.filename):
        filename, file_extension = os.path.splitext(file.filename)
        filename = random_string() + file_extension

        path = "./images/"+filename
        file.save(path)
    else:
        raise Exception('File not allowed')

    url = '/uploads/' + filename

    resp = api_resp(0, "info", url)

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/test_upload', methods=['GET', 'POST'])
def upload_file_test(): # pragma: no cover
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            raise Exception('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = request.base_url.split('/')
            file_url = url[0] + '/' + url[2] + "/uploads/" + file.filename
            return "ok: <a href=\"" + "/uploads/" + file.filename + "\">" + file_url + "</a>"
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_file('../'+app.config['UPLOAD_FOLDER']+'/' + filename)
