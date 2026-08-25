# ============================================================================
# USUARIO.PY — Model da entidade Usuário
# ============================================================================
# Representa a tabela "usuarios" do banco de dados. Cada atributo da
# classe (db.Column) vira uma coluna da tabela.
#
# Esta classe herda de DUAS classes ao mesmo tempo (herança múltipla):
#   - db.Model    -> torna a classe uma tabela do banco (via SQLAlchemy)
#   - CRUDMixin   -> dá à classe os métodos criar/listar/buscar/atualizar/deletar
# ============================================================================

from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Usuario(db.Model, CRUDMixin):
    __tablename__ = 'usuarios'  # nome real da tabela no banco MySQL

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)      # nullable=False => campo obrigatório
    email = db.Column(db.String(150), unique=True, nullable=False)  # unique => não pode repetir
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    nivel = db.Column(db.String(50))       # ex: iniciante, intermediário, avançado
    cidade = db.Column(db.String(100))

    def to_dict(self):
        """
        Converte o objeto Usuario em um dicionário Python simples,
        para que o Flask consiga transformá-lo em JSON e devolver
        como resposta da API.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
