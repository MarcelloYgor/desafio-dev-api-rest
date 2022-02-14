
from flask import current_app, jsonify
from werkzeug.exceptions import Unauthorized

import jwt

from model.usuario import Usuario

def token_required(token):

    try:
        token_info = jwt.decode(
            token,
            current_app.config['API_SECRET_KEY'],
            algorithms='HS512'
        )

        usuario = Usuario.query.filter_by(id=token_info.get('id')).first()

        if not usuario:
            raise Unauthorized

        return token_info
    except jwt.DecodeError as e:
        raise Unauthorized from e
    except jwt.ExpiredSignatureError as e:
        raise Unauthorized from e
