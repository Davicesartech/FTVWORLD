# Exemplo de Model (remover/substituir pelas Models reais do projeto)
# Cada Model deve herdar de db.Model (SQLAlchemy) e representar uma entidade do banco.

from database.connection import db


class ExemploModel(db.Model):
    __tablename__ = 'exemplo'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }
