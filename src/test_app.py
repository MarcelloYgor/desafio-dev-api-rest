
import connexion
from connexion.resolver import RestyResolver

from dao.db import db
from model import models

from sqlalchemy import event
from nacl import pwhash

from config import TestingConfig

import pytest

app = connexion.FlaskApp(__name__, specification_dir='./swagger/')

webapp = app.app

webapp.config.from_object(TestingConfig())

db.init_app(webapp)

# Inserindo usuário admin
@event.listens_for(models.Usuario.__table__, 'after_create')
def insert_admin_test(*args, **kwargs):
    usuario = models.Usuario()
    usuario.email = 'admin_test@email.com'
    senha_codificada = bytes('123@abc'.encode('utf-8'))
    hash_senha = pwhash.str(senha_codificada).decode('utf-8')
    usuario.senha = hash_senha
    usuario.admin = True

    db.session.add(usuario)
    db.session.commit()

with webapp.app_context():
    db.create_all()

app.add_api('dock_digital.yaml', resolver=RestyResolver('api'))

@pytest.fixture(scope='module')
def client():
    with webapp.test_client() as c:
        yield c

@pytest.fixture
def data():
    pytest.token = None
    pytest.token_admin = None
    pytest.portador_id = None
    pytest.conta_id = None
    pytest.transacao_id = None

def test_criacao_usuario(client):
    body = {
        "email": "fulano@email.com",
        "senha": "abc123"
    }
    response = client.post('/usuario', json=body)
    try:
        assert response.status_code == 201
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_login(client):
    headers = {
        'Authorization': 'Basic ZnVsYW5vQGVtYWlsLmNvbTphYmMxMjM='
    }
    response = client.get('/login', headers=headers)
    try:
        assert response.status_code == 200
        response_data = response.get_json()
        pytest.token = response_data.get('XAccessToken')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_criacao_portador(client):
    body = {
        "cpf": "27481361010",
        "nome": "Fulano de Tal"
    }
    headers = {
        'Authorization': f'Bearer {pytest.token}',
        'Content-Type': 'application/json'
    }
    response = client.post('/portador', headers=headers, json=body)
    try:
        assert response.status_code == 201
        response_data = response.get_json()
        pytest.portador_id = response_data.get('id')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_criacao_conta(client):
    body = {
        "saldo": 0
    }
    headers = {
        'Authorization': f'Bearer {pytest.token}',
        'Content-Type': 'application/json'
    }
    response = client.post(f'/portador/{pytest.portador_id}/conta', headers=headers, json=body)
    try:
        assert response.status_code == 201
        response_data = response.get_json()
        pytest.conta_id = response_data.get('id')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_deposito(client):
    body = {
        "transacao": "DEPOSITO",
        "valor": 1000
    }
    headers = {
        'Authorization': f'Bearer {pytest.token}',
        'Content-Type': 'application/json'
    }
    response = client.post(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}/transacao', 
            headers=headers,
            json=body)
    try:
        assert response.status_code == 201
        response_data = response.get_json()
        pytest.transacao_id = response_data.get('id')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_saque(client):
    body = {
        "transacao": "SAQUE",
        "valor": 500
    }
    headers = {
        'Authorization': f'Bearer {pytest.token}',
        'Content-Type': 'application/json'
    }
    response = client.post(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}/transacao',
            headers=headers,
            json=body)
    try:
        assert response.status_code == 201
        response_data = response.get_json()
        pytest.transacao_id = response_data.get('id')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_saque_maior_que_saldo(client):
    body = {
        "transacao": "SAQUE",
        "valor": 600
    }
    headers = {
        'Authorization': f'Bearer {pytest.token}',
        'Content-Type': 'application/json'
    }
    response = client.post(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}/transacao',
            headers=headers,
            json=body)
    try:
        assert response.status_code == 400
        response_data = response.get_json()
        pytest.transacao_id = response_data.get('id')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_extrato(client):
    headers = {
        'Authorization': f'Bearer {pytest.token}'
    }
    query = {
        'data_inicio': '2022-01-01',
        'data_fim': ''
    }
    response = client.get(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}/transacao',
            headers=headers,
            query_string=query)
    try:
        assert response.status_code == 200
        response_data = response.get_json()
        print(response_data)
        assert len(response_data) == 2
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_desativar_conta_error(client):
    headers = {
        'Authorization': f'Bearer {pytest.token}'
    }
    response = client.patch(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}', 
            headers=headers)
    try:
        assert response.status_code == 403
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_login_admin(client):
    headers = {
        'Authorization': 'Basic YWRtaW5fdGVzdEBlbWFpbC5jb206MTIzQGFiYw=='
    }
    response = client.get('/login', headers=headers)
    try:
        assert response.status_code == 200
        response_data = response.get_json()
        pytest.token_admin = response_data.get('XAccessToken')
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_desativar_conta(client):
    body = {
        "ativa": False
    }
    headers = {
        'Authorization': f'Bearer {pytest.token_admin}',
        'Content-Type': 'application/json'
    }
    response = client.patch(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}',
            headers=headers,
            json=body)
    try:
        assert response.status_code == 204
    except AssertionError as e:
        print(response.get_json())
        raise e

def test_ativar_conta(client):
    body = {
        "ativa": True
    }
    headers = {
        'Authorization': f'Bearer {pytest.token_admin}',
        'Content-Type': 'application/json'
    }
    response = client.patch(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}',
            headers=headers,
            json=body)
    try:
        assert response.status_code == 204
    except AssertionError as e:
        print(response.get_json())
        raise e

# Exclusão/fechar conta
def test_fechar_conta(client):
    headers = {
        'Authorization': f'Bearer {pytest.token}'
    }
    response = client.delete(
            f'/portador/{pytest.portador_id}/conta/{pytest.conta_id}',
            headers=headers)
    try:
        assert response.status_code == 200
    except AssertionError as e:
        print(response.get_json())
        raise e

from os import remove

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""
    def remove_test_db():
        remove('test.db')
    request.addfinalizer(remove_test_db)
