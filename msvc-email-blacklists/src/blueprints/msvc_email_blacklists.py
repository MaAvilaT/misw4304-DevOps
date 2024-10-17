from flask import Blueprint, jsonify, request

from src.blueprints.msvc_management import token_required
from src.services.email_blacklisting_service import BlacklistedEmailService

email_blacklists_blueprint = Blueprint(name='msvc_email_blacklists', import_name=__name__)


@email_blacklists_blueprint.route('/blacklists', methods=['POST'])
@token_required
def create_email_blacklisting():
    json_data = request.get_json()

    if (not json_data or
            len(json_data) != 3 or
            not all(a == b for a, b in zip(json_data.keys(), ['email', 'appUuid', 'blockedReason']))):
        return jsonify({'msg': 'bad request'}), 400

    if request.headers.getlist("X-Forwarded-For"):
        request_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        request_ip = request.remote_addr

    json_data['requestIp'] = request_ip

    to_jsonify, status_code = BlacklistedEmailService.create_email_blacklisting(data=json_data)
    return jsonify(to_jsonify), status_code


@email_blacklists_blueprint.route('/blacklists/<string:email>', methods=['GET'])
@token_required
def is_blacklisted(email):
    if not email:
        return jsonify({'msg': 'bad request'}), 400

    to_jsonify, status_code = BlacklistedEmailService.is_blacklisted(email=email)
    return jsonify(to_jsonify), status_code
