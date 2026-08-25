# ============================================================================
# PARTIDA.PY — Model da entidade Partida
# ============================================================================
# Representa uma partida de um campeonato, entre duas duplas, em uma quadra.
from models.db_instance import db
from models.crud_mixin import CRUDMixin


class Partida(db.Model, CRUDMixin):
    __tablename__ = 'partidas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fase = db.Column(db.String(50))  # ex: oitavas, quartas, semifinal, final
    placar_dupla1 = db.Column(db.Integer, default=0)
    placar_dupla2 = db.Column(db.Integer, default=0)
    data_hora = db.Column(db.DateTime)
    status = db.Column(db.String(50))  # ex: agendada, em andamento, finalizada

    id_campeonato = db.Column(db.Integer)  # chave estrangeira flexível -> Campeonato
    id_dupla1 = db.Column(db.Integer)      # chave estrangeira flexível -> Dupla
    id_dupla2 = db.Column(db.Integer)      # chave estrangeira flexível -> Dupla
    id_quadra = db.Column(db.Integer)      # chave estrangeira flexível -> Quadra

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # hasattr(..., 'isoformat') protege contra registros antigos que
        # ficaram salvos como texto puro (ex: data/hora em branco), em vez
        # de quebrar a rota inteira com AttributeError.
        if data_dict['data_hora'] and hasattr(data_dict['data_hora'], 'isoformat'):
            data_dict['data_hora'] = data_dict['data_hora'].isoformat()
        return data_dict
