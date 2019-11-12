from sqlite3 import IntegrityError

from flask import Blueprint, jsonify, request, abort
from auth.database import User, db
from datetime import datetime
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)

auth = Blueprint('auth', __name__)

'''/register register a new user'''


@auth.route('/auth/registration', methods=['POST'])
def registration():
    req = request.json
    username = req['username'].strip()
    password = req['password'].strip()
    email = req['email'].strip()
    firstname = req['firstname'].strip()
    lastname = req['lastname'].strip()
    dateofbirth = datetime.strptime(req['dateofbirth'].strip(), "%d/%m/%Y")

    new_user = User()
    new_user.username = username
    new_user.set_password(password)
    new_user.email = email
    new_user.firstname = firstname
    new_user.lastname = lastname
    new_user.dateofbirth = dateofbirth

    try:
        # COMMIT USER TO DB
        db.session.add(new_user)
        db.session.commit()

        # GENERATE TOKEN
        identity = generate_identity(new_user)
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        resp = jsonify({
            'message': 'Logged in as {}'.format(new_user.username),
        })
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
    except Exception as e:
        db.session.rollback()
        status = 409
        if 'user.username' in str(e):
            err = 'This username already exists.'
        elif 'user.email' in str(e):
            err = 'This email is already used.'
        else:
            err = 'cannot register ' + str(e)
            print(e)

        return jsonify({'err': err}), status

    return resp, 200


''' /login create the login token and refresh token for the browser session'''


@auth.route('/auth/login', methods=['POST'])
def login():
    req = request.json

    username = req['username'].strip()
    password = req['password'].strip()

    user = User.find_by_username(req['username'])

    if not user:
        return {'err': 'User {} not exist'.format(username)}, 401

    if user.check_password(password):
        identity = generate_identity(user)
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        resp = jsonify({
            'message': 'Logged in as {}'.format(user.username),
        })
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

    else:
        return {'message': 'Wrong credentials'}, 401


''' /logout Reset the browser cache, the current login token will expire in 15 min and the refresh token in 30 days'''


@auth.route('/auth/logout', methods=['POST'])
@jwt_required
def logout():
    identity = get_jwt_identity()
    if identity:
        resp = jsonify({
            'message': 'Logged out {}'.format(identity['username']),
        })
        unset_jwt_cookies(resp)
        return resp, 200
    else:
        abort(401)


''' /token_refresh Refresh the current expired login token '''


@auth.route('/auth/token_refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


@auth.route('/test/auth/all_users', methods=['GET'])
def all_users():
    return jsonify(User.return_all())


@auth.route('/test/auth/all_users', methods=['DELETE'])
def delete_all_users():
    return jsonify(User.delete_all())


@auth.route('/test/auth/secret_resource', methods=['GET'])
@jwt_required
def secret_resource():
    identity = get_jwt_identity()
    return jsonify({'message': 'Hello, {}'.format(identity['username'])})


def generate_identity(user):
    return {"username": user.username, "password": user.password, "id": user.id}
