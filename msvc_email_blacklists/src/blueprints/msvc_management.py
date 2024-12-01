import logging
from functools import wraps

from flask import Blueprint, jsonify, request
from services.authentication_service import AuthenticationService

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

management_blueprint = Blueprint(name='management', import_name=__name__)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt = request.headers.get('Authorization')
        logging.debug(f'Received JWT: {jwt}')
        if not AuthenticationService.is_valid_jwt(jwt):
            logging.warning('Unauthorized access attempt')
            return jsonify(message='Unauthorized'), 401
        return f(*args, **kwargs)

    return decorated_function


@management_blueprint.route('/health', methods=['GET'])
def health():
    logging.info('Health check endpoint called')
    return 'pong', 200
