import datetime

from flask import Blueprint, request, json, Response
from flask_login import login_required, current_user

from ChangePop.exeptions import JSONExceptionHandler, UserNotPermission, ProductException
from ChangePop.models import Products, Bids, Reports, Users
from ChangePop.utils import api_resp

bp = Blueprint('reports', __name__)

CORS(bp)


@bp.route('/report', methods=['POST'])
@login_required
def new_report():
    if not request.is_json:
        raise JSONExceptionHandler()

    content = request.get_json()

    user_id = int(content["user_id"])
    if 'product_id' in content:
        product_id = int(content["product_id"])
    else:
        product_id = None
    reason = str(content["reason"])

    id = Reports.new_report(user_id, product_id, reason)

    resp = api_resp(0, "info", str(id))

    return Response(json.dumps(resp), status=200, content_type='application/json')


@bp.route('/reports', methods=['GET'])
@login_required
def get_report():

    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    reports = Reports.list()

    reports_list = []

    for report in reports:
        item = {
            "id": str(report.id),
            "user_id": str(report.user_id),
            "user_nick": str(Users.get_nick(report.user_id)),
            "reason": str(report.reason),
            "date": str(report.report_date),
            "product_id": str(report.product_id)
        }

        reports_list.append(item)

    json_reports = {"length": len(reports_list), "list": reports_list}

    return Response(json.dumps(json_reports), status=200, content_type='application/json')


@bp.route('/report/<int:id>', methods=['DELETE'])
@login_required
def delete_report(id):
    if not current_user.is_mod:
        raise UserNotPermission(str(current_user.nick))

    Reports.delete_by_id(id)

    resp = api_resp(0, "info", "Report " + str(id) + "deleted")

    return Response(json.dumps(resp), status=200, content_type='application/json')

