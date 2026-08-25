# ============================================================================
# CAMPEONATO.PY — Model da entidade Campeonato
# ============================================================================
from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Campeonato(db.Model, CRUDMixin):
    __tablename__ = 'campeonatos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    data = db.Column(db.Date)
    horario = db.Column(db.Time)
    categoria = db.Column(db.String(50))
    nivel = db.Column(db.String(50))
    vagas_total = db.Column(db.Integer)
    vagas_disponiveis = db.Column(db.Integer)
    status = db.Column(db.String(50))  # ex: aberto, encerrado, cancelado

    def to_dict(self):
        """
        Converte o objeto em dicionário para virar JSON.
        Datas e horários (tipos especiais do Python) precisam ser
        convertidos manualmente para texto (isoformat), pois o
        conversor de JSON do Flask não sabe lidar com esses tipos
        sozinho.
        """
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # hasattr(..., 'isoformat') protege contra registros antigos que
        # ficaram salvos como texto puro (ex: data em branco), em vez de
        # quebrar a rota inteira com AttributeError.
        if data_dict['data'] and hasattr(data_dict['data'], 'isoformat'):
            data_dict['data'] = data_dict['data'].isoformat()
        if data_dict['horario'] and hasattr(data_dict['horario'], 'strftime'):
            data_dict['horario'] = data_dict['horario'].strftime('%H:%M:%S')
        return data_dict
