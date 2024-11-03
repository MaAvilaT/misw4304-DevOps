from flask import Blueprint, jsonify, request
from functools import wraps

from src.services.authentication_service import AuthenticationService

management_blueprint = Blueprint(name='management', import_name=__name__)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        jwt = request.headers.get('Authorization')
        if not AuthenticationService.is_valid_jwt(jwt):
            return jsonify(message='Unauthorized'), 401
        return f(*args, **kwargs)
    return decorated_function


@management_blueprint.route('/health', methods=['GET'])
def health():
    return 'pong', 200
