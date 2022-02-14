
from flask import request, jsonify

from dao.db import db
from model.portador import Portador

def cria_portador(token_info):

    body = request.get_json()

    portador = Portador.query.filter_by(
            cpf=body['cpf']).first()

    if portador:
        return jsonify(
            {
                'message': 'Portador já cadastrado'
            }
        ), 400

    portador = Portador()
    portador.from_dict(body)
    portador.usuario_id = token_info.get('id')

    if not portador.cpf_valido():
        return jsonify(
            {
                'message': 'CPF inválido'
            }
        ), 400

    db.session.add(portador)
    db.session.commit()

    portador = portador.to_dict()

    return portador, 201

def exclui_portador(token_info):
    
    portador = Portador.query.filter_by(
            id=token_info.get('id')).first()

    if not portador:
        return jsonify(
            {
                'message': 'Portador não encontrado'
            }
        ), 400

    db.session.delete(portador)
    db.session.commit()

    return jsonify(
        {
            'message': 'Portador excluído com sucesso'
        }
    ), 200
