# ============================================================================
# APP.PY — Ponto de entrada da aplicação Flask
# ============================================================================
# Este é o arquivo que efetivamente "liga" o servidor. Ele:
#   1. Cria a aplicação Flask
#   2. Configura a conexão com o banco de dados MySQL
#   3. Registra todas as rotas (CRUD básico + relatórios)
#   4. Inicia o servidor local
#
# Para rodar: dentro da pasta "backend", executar "python app.py"
# ============================================================================
from flask import Flask
from flask_cors import CORS

from models import db
from controllers.controllers import registrar_rotas_crud
from controllers.report_controller import registrar_rotas_relatorios

app = Flask(__name__)

# CORS = Cross-Origin Resource Sharing. Sem isso, o navegador BLOQUEIA
# requisições vindas do frontend (arquivo HTML aberto localmente) para
# a API (rodando em outro endereço/porta), por questões de segurança.
CORS(app)

# ------------------------------------------------------------
# CONEXÃO COM O BANCO DE DADOS MySQL (via XAMPP)
# ------------------------------------------------------------
# Formato da URI: mysql+pymysql://usuario:senha@host/nome_do_banco
# O XAMPP, por padrão, usa usuário "root" sem senha.
# Se o seu ambiente usa outro usuário/senha/nome de banco, ajuste aqui.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ftvworld'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # desativa um recurso não usado, economiza memória

db.init_app(app)  # conecta a instância do SQLAlchemy a esta aplicação Flask

with app.app_context():
    db.create_all()  # cria as 7 tabelas no banco automaticamente, caso ainda não existam

# ------------------------------------------------------------
# REGISTRO DAS ROTAS
# ------------------------------------------------------------

# Rotas do CRUD básico: /api/usuarios, /api/campeonatos, /api/quadras,
# /api/inscricoes, /api/duplas, /api/partidas, /api/notificacoes
# (Controllers como classes -> Services por caso de uso -> CRUD na Model)
registrar_rotas_crud(app)

# Rotas das funcionalidades avançadas (relatórios via procedures):
# /api/relatorios/campeonatos-disponiveis, /ranking-duplas, etc.
# (Controller como classe -> Service -> Repository -> Procedure no banco)
registrar_rotas_relatorios(app)


if __name__ == '__main__':
    # debug=True reinicia o servidor automaticamente a cada alteração
    # de código, e mostra mensagens de erro detalhadas — útil durante
    # o desenvolvimento, mas NÃO deve ser usado em produção.
    app.run(debug=True)
