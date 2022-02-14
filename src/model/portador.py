
from sqlalchemy import Column, Sequence, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from dao.db import db

class Portador(db.Model):
    __tablename__ = 'portador'

    id = Column(
            Integer,
            Sequence('portador_id_seq'),
            primary_key=True)
    usuario_id = Column(
            Integer,
            ForeignKey('usuario.id', ondelete='CASCADE')
    )
    cpf = Column(String(11), unique=True)
    nome = Column(String(128))

    usuario = relationship('Usuario')
    contas = relationship(
            'Conta',
            cascade='all, delete-orphan')

    def cpf_valido(self):
        cpf = [int(char) for char in self.cpf if char.isdigit()]

        if len(cpf) != 11:
            return False

        if cpf == cpf[::-1]:
            return False

        for i in range(9, 11):
            value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False
        return True

    def from_dict(self, obj):
        self.cpf = obj.get('cpf')
        self.nome = obj.get('nome')

    def to_dict(self):
        return {
            'id': self.id,
            'cpf': self.cpf,
            'nome': self.nome
        }
