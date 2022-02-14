
from flask import request, jsonify

from datetime import datetime

from dao.db import db
from model.conta import Conta
from model.transacao import Transacao
from model.conta import Conta
from model.portador import Portador
from model.usuario import Usuario

from utils.exceptions import SemSaldoException

def cria_transacao(portador_id, conta_id, token_info):

    body = request.get_json()

    # Lock (with_for_update) no registro da conta para garantir ordem correta dos registros de transações
    conta = Conta.query.filter(
            Conta.id == conta_id,
            Conta.portador).join(Portador).filter(
                Portador.id == portador_id,
                Portador.usuario).join(Usuario).filter(
                    Usuario.id == token_info.get('id')).populate_existing().with_for_update(
                        of=Conta).first()

    if not conta:
        return jsonify(
            {
                'message': 'Conta inválida'
            }
        ), 400

    transacao = Transacao()
    transacao.conta_id = conta_id
    transacao.from_dict(body)

    if transacao.eDeposito():
        conta.deposita(body['valor'])
    if transacao.eSaque():
        try:
            conta.saca(body['valor'])
        except SemSaldoException:
            db.session.rollback()
            return jsonify(
                {
                    'message': 'Valor de saque informado não disponível em saldo'
                }
            ), 400

    db.session.add(transacao)
    db.session.commit()

    transacao = transacao.to_dict()

    return transacao, 201

def busca_transacao(portador_id, conta_id, id, token_info):

    transacao = Transacao.query.filter(
            Transacao.id == id,
            Transacao.conta).join(Conta).filter(
                Conta.id == conta_id,
                Conta.portador).join(Portador).filter(
                    Portador.portador_id == portador_id,
                    Portador.usuario).join(Usuario).filter(
                        Usuario.id == token_info.get('id')).first()

    if not transacao:
        return jsonify(
            {
                'message': 'Transação não encontrada'
            }
        ), 400

    transacao = transacao.to_dict()

    return transacao, 200

def lista_transacao(portador_id, conta_id, data_inicio, data_fim, token_info):

    conta = Conta.query.filter(
                Conta.id == conta_id,
                Conta.portador).join(Portador).filter(
                    Portador.id == portador_id,
                    Portador.usuario).join(Usuario).filter(
                        Usuario.id == token_info.get('id')).first()

    if data_inicio and data_fim:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim =  datetime.strptime(data_fim, '%Y-%m-%d')
        except:
            return jsonify({
                'message': 'A data deve estar no formato \'AAAA-MM-DD\''
            }), 400

        transacoes = Transacao.query.filter(
                Transacao.data_hora >= data_inicio,
                Transacao.data_hora <= data_fim,
                Transacao.conta_id == conta.id).all()
    elif data_inicio:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        except:
            return jsonify({
                'message': 'A data deve estar no formato \'AAAA-MM-DD\''
            }), 400

        transacoes = Transacao.query.filter(
                Transacao.data_hora >= data_inicio,
                Transacao.conta_id == conta.id).all()
    elif data_fim:
        try:
            data_fim =  datetime.strptime(data_fim, '%Y-%m-%d')
        except:
            return jsonify({
                'message': 'A data deve estar no formato \'AAAA-MM-DD\''
            }), 400

        transacoes = Transacao.query.filter(
                Transacao.data_hora <= data_fim,
                Transacao.conta_id == conta.id).all()
    else:
        transacoes = Transacao.query.filter_by(conta_id == conta.id).all()

    transacoes = [transacao.to_dict() for transacao in transacoes]

    return transacoes, 200
