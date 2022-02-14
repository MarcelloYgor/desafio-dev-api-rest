
from datetime import datetime, timedelta
import time

from flask import request, current_app, jsonify
from werkzeug.exceptions import Unauthorized

from nacl import pwhash
from nacl.exceptions import InvalidkeyError

import jwt

from model.usuario import Usuario

def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        raise Unauthorized

    usuario = Usuario.query.filter_by(email=auth.username).first()

    if not usuario:
        raise Unauthorized

    encoded_password = bytes(auth.password.encode('utf-8'))

    try:
        if pwhash.verify(bytes(usuario.senha.encode('utf-8')), encoded_password):
            token = jwt.encode(
                {
                    'id': usuario.id,
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                },
                current_app.config['API_SECRET_KEY'],
                algorithm='HS512'
            )

            return jsonify(
                {
                    'message': 'Login com sucesso',
                    'XAccessToken': token
                }
            ), 200
    except InvalidkeyError:
        time.sleep(3)

    raise Unauthorized
