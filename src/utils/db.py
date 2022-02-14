
from model.conta import Conta

def numero_nova_conta():
    ultima_conta = Conta.query.order_by(Conta.numero.desc()).first()

    if ultima_conta:
        return ultima_conta.numero + 1
    else:
        return 1
