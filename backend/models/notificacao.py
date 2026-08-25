# ============================================================================
# NOTIFICACAO.PY — Model da entidade Notificação
# ============================================================================
from datetime import datetime
from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Notificacao(db.Model, CRUDMixin):
    __tablename__ = 'notificacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensagem = db.Column(db.String(255), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.Date, default=datetime.utcnow)

    id_usuario = db.Column(db.Integer)  # chave estrangeira flexível -> Usuario

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data_dict['data_envio']:
            data_dict['data_envio'] = data_dict['data_envio'].isoformat()
        return data_dict
