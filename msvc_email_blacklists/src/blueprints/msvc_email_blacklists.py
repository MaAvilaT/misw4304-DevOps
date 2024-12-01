import logging

from blueprints.msvc_management import token_required
from flask import Blueprint, jsonify, request
from services.email_blacklisting_service import BlacklistedEmailService

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

email_blacklists_blueprint = Blueprint(name='msvc_email_blacklists', import_name=__name__)


@email_blacklists_blueprint.route('/blacklists', methods=['POST'])
@token_required
def create_email_blacklisting():
    json_data = request.get_json()
    logging.debug(f'Received request data: {json_data}')

    if (not json_data or
            len(json_data) != 3 or
            not all(a == b for a, b in zip(json_data.keys(), ['email', 'appUuid', 'blockedReason']))):
        logging.warning('Bad request: Invalid JSON data')
        return jsonify({'msg': 'bad request'}), 400

    if request.headers.getlist("X-Forwarded-For"):
        request_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        request_ip = request.remote_addr

    json_data['requestIp'] = request_ip
    logging.debug(f'Request IP: {request_ip}')

    is_blacklisted, is_blacklisted_sta = BlacklistedEmailService.is_blacklisted(email=json_data['email'])
    if is_blacklisted_sta == 'true':
        logging.info(f'Email {json_data["email"]} already blacklisted')
        return jsonify({'msg': 'email already blacklisted'}), 409

    to_jsonify, status_code = BlacklistedEmailService.create_email_blacklisting(data=json_data)
    logging.debug(f'Blacklist creation response: {to_jsonify}, status code: {status_code}')
    return jsonify(to_jsonify), status_code


@email_blacklists_blueprint.route('/blacklists/<string:email>', methods=['GET'])
@token_required
def is_blacklisted(email):
    if not email:
        logging.warning('Bad request: No email provided')
        return jsonify({'msg': 'bad request'}), 400

    to_jsonify, status_code = BlacklistedEmailService.is_blacklisted(email=email)
    logging.debug(f'Blacklist check response for {email}: {to_jsonify}, status code: {status_code}')
    return jsonify(to_jsonify), status_code
