from flask import jsonify
from flask_jwt_extended import create_access_token

from auth.database import User


def test_1_signup(client, database):
    loginreq = {
        "username": "giobarty",
        "password": "mario123",
        "dateofbirth": "25/08/1996",
        "firstname": "giovanni",
        "lastname": "bartolomeo",
        "email": "ggg@gmail.com"
    }

    reply = client.post('/auth/registration', json=loginreq)
    assert reply.status_code == 200

    token_cookie = reply.headers.getlist('Set-Cookie')
    assert token_cookie is not None

def test_2_signup(client):
    loginreq = {
        "username": "giobarty",
        "password": "mario123",
        "dateofbirth": "25/08/1996",
        "firstname": "giovanni",
        "lastname": "bartolomeo",
        "email": "ggg@gmail.com"
    }

    reply = client.post('/auth/registration', json=loginreq)
    reply = client.post('/auth/registration', json=loginreq)
    assert reply.status_code == 409

def test_3_login(client,database):
    loginreq = {
        "username": "test1",
        "password": "test1123",
    }

    reply = client.post('/auth/login', json=loginreq)
    assert reply.status_code == 200

    token_cookie = reply.headers.getlist('Set-Cookie')
    assert token_cookie is not None

def test_4_secret(client,database):
    loginreq = {
        "username": "test1",
        "password": "test1123",
    }

    reply = client.post('/auth/login', json=loginreq)
    token_cookie = reply.headers.getlist('Set-Cookie')
    assert reply.status_code == 200

    headers = {
        'Authorization': 'Bearer {}'.format(token_cookie[0])
    }
    reply = client.get('/test/auth/secret_resource', headers=headers)
    assert reply.status_code == 200

def test_5_secret(client,database):

    reply = client.get('/test/auth/secret_resource')
    assert reply.status_code == 401

