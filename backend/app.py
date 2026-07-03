import os
from flask import Flask
from flask_cors import CORS
from models.models import db, Usuario, Campeonato, Quadra, Inscricao, Dupla, Partida, Notificacao
from controllers.controllers import create_crud_blueprint

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')

def create_app():
    app = Flask(__name__)
    CORS(app)

    os.makedirs(DATABASE_DIR, exist_ok=True)

    db_path = os.path.join(DATABASE_DIR, 'futworld.db').replace('\\', '/')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(create_crud_blueprint('usuarios', Usuario))
    app.register_blueprint(create_crud_blueprint('campeonatos', Campeonato))
    app.register_blueprint(create_crud_blueprint('quadras', Quadra))
    app.register_blueprint(create_crud_blueprint('inscricoes', Inscricao))
    app.register_blueprint(create_crud_blueprint('duplas', Dupla))
    app.register_blueprint(create_crud_blueprint('partidas', Partida))
    app.register_blueprint(create_crud_blueprint('notificacoes', Notificacao))

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)