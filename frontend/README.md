FutWorld 🏐

Sistema de gerenciamento de campeonatos de futevôlei (cadastro de usuários, campeonatos, quadras, inscrições, duplas, partidas e notificações).

Projeto acadêmico desenvolvido em Flask (backend) seguindo a arquitetura em camadas Model → Service → Controller, com frontend em HTML/JS + Tailwind consumindo a API.

📌 Etapa atual: CRUD básico das Models principais

Nesta etapa foi implementado o CRUD completo (criar, listar, buscar, atualizar, excluir) para todas as entidades da modelagem de domínio.

Models implementadas

Todas em backend/models/models.py, herdando de db.Model (Flask-SQLAlchemy):

Model	Tabela	Descrição
Usuario	usuarios	Jogadores/administradores do sistema
Campeonato	campeonatos	Campeonatos cadastrados
Quadra	quadras	Locais/quadras disponíveis
Inscricao	inscricoes	Inscrições de duplas em campeonatos
Dupla	duplas	Duplas formadas por dois usuários
Partida	partidas	Partidas de um campeonato
Notificacao	notificacoes	Notificações enviadas aos usuários

Cada Model possui o método to_dict() para serialização em JSON.

Services (separados por caso de uso)

Em backend/services/crud_service.py. Cada classe representa um caso de uso do CRUD e é reutilizada por todas as Models:

CreateService — cria um novo registro (com tratamento automático de campos de data/hora)
ListService — lista todos os registros de uma entidade
FindByIdService — busca um registro por ID
UpdateService — atualiza um registro existente
DeleteService — remove um registro

Nota de arquitetura: optamos por Services genéricos parametrizados por model_class, em vez de uma classe por Model (ex: CreateUsuarioService). Isso evita duplicação de código, já que a lógica de cada operação CRUD é idêntica entre entidades — mudando apenas a Model manipulada. Cada caso de uso (criar, listar, buscar, atualizar, excluir) continua isolado em sua própria classe.

Controllers e rotas da API

Em backend/controllers/controllers.py, a função create_crud_blueprint(name, model_class) gera dinamicamente um Blueprint Flask com as rotas REST para cada Model.

Todas as rotas seguem o padrão /api/<entidade>:

Método	Rota	Ação
POST	/api/<entidade>	Criar registro
GET	/api/<entidade>	Listar todos os registros
GET	/api/<entidade>/<id>	Buscar registro por ID
PUT	/api/<entidade>/<id>	Atualizar registro
DELETE	/api/<entidade>/<id>	Excluir registro

Entidades disponíveis (<entidade>): usuarios, campeonatos, quadras, inscricoes, duplas, partidas, notificacoes.

Exemplo: GET http://127.0.0.1:5000/api/campeonatos

Frontend

Em frontend/index.html: página administrativa única (HTML + JS puro + Tailwind) que consome a API e permite, para qualquer entidade selecionada no menu:

Cadastrar um novo registro (modal com formulário)
Listar todos os registros em tabela
Editar um registro existente
Excluir um registro

Os campos de cada formulário são gerados dinamicamente a partir do objeto schemas, que mapeia os atributos de cada Model.

🗂 Estrutura do projeto
FTVWORLD/
├── backend/
│   ├── app.py                     # ponto de entrada, registra os Blueprints
│   ├── models/
│   │   └── models.py               # Models (SQLAlchemy)
│   ├── services/
│   │   └── crud_service.py         # Services genéricos por caso de uso
│   ├── controllers/
│   │   └── controllers.py          # Controllers/Blueprints com as rotas
│   └── database/
│       └── futworld.db             # banco SQLite (gerado automaticamente)
└── frontend/
    └── index.html                  # tela administrativa (CRUD)
▶️ Como executar o projeto
Pré-requisitos
Python 3.10+
pip
Backend
bash
cd backend
pip install flask flask_sqlalchemy flask_cors
python app.py

O servidor sobe em http://127.0.0.1:5000. O banco SQLite (futworld.db) é criado automaticamente na primeira execução, dentro de backend/database/.

Frontend

Basta abrir o arquivo frontend/index.html diretamente no navegador (ou servir com uma extensão tipo Live Server). Ele já está configurado para consumir a API em http://127.0.0.1:5000/api.

Importante: o backend precisa estar rodando antes de abrir o frontend, senão as requisições falham.

👥 Equipe
[Adicionar nomes dos integrantes do grupo]
🔜 Próximas etapas
Implementação de funcionalidades avançadas (filtros, buscas, ordenações, relatórios) via procedures no banco de dados, acessadas pela camada Repository.
