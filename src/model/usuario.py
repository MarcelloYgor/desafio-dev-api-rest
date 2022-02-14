
from sqlalchemy import Boolean, Column, Sequence, Integer, String
from sqlalchemy.orm import relationship

from nacl import pwhash

from dao.db import db

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = Column(
            Integer,
            Sequence('usuario_id_seq'),
            primary_key=True)
    email = Column(String(128), unique=True)
    senha = Column(String(256))
    admin = Column(Boolean)

    portador = relationship(
            'Portador',
            cascade='all, delete-orphan')

    def __init__(self):
        self.admin = False

    def from_dict(self, obj):
        self.email = obj.get('email')
        senha_codificada = bytes(obj.get('senha').encode('utf-8'))
        hash_senha = pwhash.str(senha_codificada).decode('utf-8')
        self.senha = hash_senha

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email
        }
