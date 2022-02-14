
from flask import request, jsonify

from dao.db import db
from model.usuario import Usuario

def cria_usuario():

    body = request.get_json()

    usuario = Usuario.query.filter_by(email=body.get('email')).first()

    if usuario:
        return jsonify(
            {'message': 'E-mail já cadastrado'}
        ), 400

    usuario = Usuario()
    usuario.from_dict(body)
    db.session.add(usuario)
    db.session.commit()

    usuario = usuario.to_dict()

    return usuario, 201
