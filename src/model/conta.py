
from sqlalchemy import Column, Sequence, ForeignKey, Integer, Numeric, Boolean
from sqlalchemy.orm import relationship

from dao.db import db
from utils.exceptions import SemSaldoException

class Conta(db.Model):
    __tablename__ = 'conta'

    id = Column(
            Integer,
            Sequence('conta_id_seq'),
            primary_key=True)
    portador_id = Column(
            Integer,
            ForeignKey('portador.id', ondelete='CASCADE'))
    saldo = Column(Numeric)
    numero = Column(
            Integer, 
            Sequence('conta_numero_seq'))
    agencia = Column(Integer)
    ativa = Column(Boolean)

    portador = relationship('Portador')
    transacao = relationship(
            'Transacao',
            cascade='all, delete-orphan')

    def __init__(self):
        self.saldo = 0
        self.agencia = 1
        self.ativa = True

    def deposita(self, valor):

        self.saldo += valor

    def saca(self, valor):

        if self.saldo - valor < 0:
            raise(SemSaldoException())

        self.saldo -= valor

    def from_dict(self, obj):
        self.portador_id = obj.get('portador_id')

    def to_dict(self):
        return {
            'id': self.id,
            'portador_id': self.portador_id,
            'saldo': self.saldo,
            'numero': self.numero,
            'agencia': self.agencia,
            'ativa': self.ativa
        }
