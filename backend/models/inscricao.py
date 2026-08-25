# ============================================================================
# INSCRICAO.PY — Model da entidade Inscrição
# ============================================================================
# Representa a inscrição de uma Dupla em um Campeonato.
from datetime import datetime
from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Inscricao(db.Model, CRUDMixin):
    __tablename__ = 'inscricoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50))  # ex: pendente, confirmada, cancelada
    data_inscricao = db.Column(db.Date, default=datetime.utcnow)

    id_campeonato = db.Column(db.Integer)  # chave estrangeira flexível -> Campeonato
    id_dupla = db.Column(db.Integer)       # chave estrangeira flexível -> Dupla

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data_dict['data_inscricao']:
            data_dict['data_inscricao'] = data_dict['data_inscricao'].isoformat()
        return data_dict
