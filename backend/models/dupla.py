# ============================================================================
# DUPLA.PY — Model da entidade Dupla
# ============================================================================
# Representa a dupla formada por dois usuários (jogadores).
from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Dupla(db.Model, CRUDMixin):
    __tablename__ = 'duplas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario1 = db.Column(db.Integer)  # chave estrangeira flexível -> Usuario
    id_usuario2 = db.Column(db.Integer)  # chave estrangeira flexível -> Usuario
    categoria = db.Column(db.String(50))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
