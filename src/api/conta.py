
from flask import request, jsonify

from dao.db import db
from model.conta import Conta
from model.portador import Portador
from model.usuario import Usuario

from utils.permission import admin_only
from utils.db import numero_nova_conta

def cria_conta(portador_id, token_info):

    body = request.get_json()

    conta = Conta.query.filter_by(
            portador_id=portador_id).first()

    if conta:
        return jsonify(
            {
                'message': 'Conta já cadastrada'
            }
        ), 400

    conta = Conta()
    conta.from_dict(body)
    conta.portador_id = portador_id
    conta.numero = numero_nova_conta()
    db.session.add(conta)
    db.session.commit()

    conta = conta.to_dict()

    return conta, 201

def busca_conta(portador_id, id, token_info):

    conta = Conta.query.filter(
            Conta.id == id,
            Conta.portador_id == portador_id,
            Conta.portador).join(Portador).filter(
                Portador.usuario).join(Usuario).filter(
                    Usuario.id == token_info.get('id')).first()

    if not conta:
        return jsonify(
            {
                'message': 'Conta não encontrada'
            }
        ), 400

    conta = conta.to_dict()

    return conta, 200

def exclui_conta(portador_id, id, token_info):

    conta = Conta.query.filter(
            Conta.id == id,
            Conta.portador_id == portador_id,
            Conta.portador).join(Portador).filter(
                Portador.usuario).join(Usuario).filter(
                    Usuario.id == token_info.get('id')).first()

    if not conta:
        return jsonify(
            {
                'message': 'Conta não encontrada'
            }
        ), 400

    db.session.delete(conta)
    db.session.commit()

    return jsonify(
        {
            'message': 'Conta excluída com sucesso'
        }
    ), 200

@admin_only()
def altera_status_conta(portador_id, id, token_info):

    body = request.get_json()

    conta = Conta.query.filter(
            Conta.id == id,
            Conta.portador_id == portador_id).first()

    if not conta:
        return jsonify(
            {
                'message': 'Conta não encontrada'
            }
        ), 400

    conta.ativa = body['ativa']
    db.session.add(conta)
    db.session.commit()

    conta = conta.to_dict()

    return conta, 204
