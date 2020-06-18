"""Routes for main pages."""
from flask import Blueprint, jsonify, request, url_for
from ..auth.models import db, User
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.http import HTTP_STATUS_CODES


# Blueprint Configuration

api_bp = Blueprint('api_bp',
                    __name__)


# BASIC AUTH and TOKENS methods

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(name, password):
    user = User.query.filter_by(name=name).first()
    if user and user.check_password(password):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


# TOKENS routes

@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})

@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204


# API routes

@api_bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
#@basic_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@api_bp.route('/users', methods=['GET'])
#@token_auth.login_required
@basic_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query)
    return jsonify(data)

@api_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include name, email and password fields')
    if User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api_bp.get_user', id=user.id)
    return response

@api_bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
#@basic_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != user.name and \
            User.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


# ERROR reports

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)
