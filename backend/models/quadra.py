# ============================================================================
# QUADRA.PY — Model da entidade Quadra
# ============================================================================
from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Quadra(db.Model, CRUDMixin):
    __tablename__ = 'quadras'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    numero_quadras = db.Column(db.Integer)
    contato = db.Column(db.String(50))

    # "Chave estrangeira flexível": guarda o ID de um Usuario responsável,
    # mas sem usar db.ForeignKey formalmente (opção de modelagem mais simples
    # adotada neste projeto).
    id_responsavel = db.Column(db.Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
