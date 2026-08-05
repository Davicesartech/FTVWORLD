from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    nivel = db.Column(db.String(50))
    cidade = db.Column(db.String(100))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Campeonato(db.Model):
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
    status = db.Column(db.String(50))

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data_dict['data']: data_dict['data'] = data_dict['data'].isoformat()
        if data_dict['horario']: data_dict['horario'] = data_dict['horario'].strftime('%H:%M:%S')
        return data_dict

class Quadra(db.Model):
    __tablename__ = 'quadras'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    numero_quadras = db.Column(db.Integer)
    contato = db.Column(db.String(50))
    id_responsavel = db.Column(db.Integer)  # Chave estrangeira flexível para Usuario

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Inscricao(db.Model):
    __tablename__ = 'inscricoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(50))
    data_inscricao = db.Column(db.Date, default=datetime.utcnow)
    id_campeonato = db.Column(db.Integer)  # Chave estrangeira flexível
    id_dupla = db.Column(db.Integer)       # Chave estrangeira flexível

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data_dict['data_inscricao']: data_dict['data_inscricao'] = data_dict['data_inscricao'].isoformat()
        return data_dict

class Dupla(db.Model):
    __tablename__ = 'duplas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario1 = db.Column(db.Integer)  # Chave estrangeira flexível
    id_usuario2 = db.Column(db.Integer)  # Chave estrangeira flexível
    categoria = db.Column(db.String(50))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Partida(db.Model):
    __tablename__ = 'partidas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fase = db.Column(db.String(50))
    placar_dupla1 = db.Column(db.Integer, default=0)
    placar_dupla2 = db.Column(db.Integer, default=0)
    data_hora = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    id_campeonato = db.Column(db.Integer)  # Chave estrangeira flexível
    id_dupla1 = db.Column(db.Integer)      # Chave estrangeira flexível
    id_dupla2 = db.Column(db.Integer)      # Chave estrangeira flexível 
    id_quadra = db.Column(db.Integer)      # Chave estrangeira flexível 

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data_dict['data_hora']: data_dict['data_hora'] = data_dict['data_hora'].isoformat()
        return data_dict

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensagem = db.Column(db.String(255), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.Date, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer)  # Chave estrangeira flexível

    def to_dict(self):
        data_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if data_dict['data_envio']: data_dict['data_envio'] = data_dict['data_envio'].isoformat()
        return data_dict
