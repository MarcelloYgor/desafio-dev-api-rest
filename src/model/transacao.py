
from sqlalchemy import Column, Sequence, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship

from enum import Enum
from datetime import datetime

from dao.db import db

class TransacaoEnum(Enum):
    deposito = 'DEPOSITO'
    saque = 'SAQUE'

class Transacao(db.Model):
    __tablename__ = 'transacao'

    id = Column(
            Integer,
            Sequence('transacao_id_seq'),
            primary_key=True)
    conta_id = Column(
            Integer,
            ForeignKey('conta.id', ondelete='CASCADE'))
    transacao = Column(String(20))
    valor = Column(Numeric)
    data_hora = Column(DateTime())

    conta = relationship('Conta')

    def eDeposito(self):
        return TransacaoEnum.deposito.value == self.transacao

    def eSaque(self):
        return TransacaoEnum.saque.value == self.transacao

    def from_dict(self, obj):
        self.transacao = TransacaoEnum(obj.get('transacao')).value
        self.valor = obj.get('valor')
        self.data_hora = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'conta_id': self.conta_id,
            'transacao': self.transacao,
            'valor': self.valor,
            'data_hora': self.data_hora            
        }
