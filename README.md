FutWorld — Pacote completo (código + explicação para apresentação)
Este pacote contém todos os arquivos necessários para rodar o backend e o frontend do zero, já com a arquitetura corrigida conforme pedido pelo professor, e totalmente comentado em português, pensado para ler e explicar durante a apresentação à banca.

Funcionalidades Implementadas
As 10 funcionalidades abaixo estão implementadas de ponta a ponta (Interface → API Flask → Controller → Service → Model/Repository → Banco de Dados):

Cadastrar Usuário — tela de CRUD (Usuários) → POST /api/usuarios → UsuarioController → CreateUsuarioService → Usuario.criar()
Listar Usuários — tela de CRUD (Usuários) → GET /api/usuarios → UsuarioController → ListUsuarioService → Usuario.listar()
Atualizar Usuário — tela de CRUD (Usuários) → PUT /api/usuarios/<id> → UsuarioController → UpdateUsuarioService → Usuario.atualizar()
Excluir Usuário — tela de CRUD (Usuários) → DELETE /api/usuarios/<id> → UsuarioController → DeleteUsuarioService → Usuario.deletar()
Cadastrar Campeonato — tela de CRUD (Campeonatos) → POST /api/campeonatos → CampeonatoController → CreateCampeonatoService → Campeonato.criar()
Consultar Campeonatos Disponíveis (filtro opcional por categoria e nível) — tela de Relatórios → GET /api/relatorios/campeonatos-disponiveis → CampeonatosDisponiveisController → CampeonatosDisponiveisService → ReportRepository → procedure sp_campeonatos_disponiveis
Ranking de Duplas (por número de vitórias) — tela de Relatórios → GET /api/relatorios/ranking-duplas → RankingDuplasController → RankingDuplasService → ReportRepository → procedure sp_ranking_duplas
Listar Inscritos de um Campeonato — tela de Relatórios → GET /api/relatorios/inscritos-campeonato/<id> → InscritosCampeonatoController → InscritosCampeonatoService → ReportRepository → procedure sp_inscritos_campeonato
Histórico de Partidas de um Usuário (com adversário e placar) — tela de Relatórios → GET /api/relatorios/historico-usuario/<id> → HistoricoUsuarioController → HistoricoPartidasUsuarioService → ReportRepository → procedure sp_historico_partidas_usuario
Quadras Mais Utilizadas (quantidade de partidas por quadra) — tela de Relatórios → GET /api/relatorios/quadras-mais-utilizadas → QuadrasMaisUtilizadasController → QuadrasMaisUtilizadasService → ReportRepository → procedure sp_quadras_mais_utilizadas
As demais operações de CRUD (Campeonato, Quadra, Inscrição, Dupla, Partida, Notificação — listar/buscar/atualizar/excluir) também estão implementadas e funcionando, seguindo exatamente o mesmo padrão das funcionalidades 1 a 5 acima; a lista de 10 foi selecionada para cobrir tanto o fluxo de Model (CRUD via CRUDMixin) quanto o fluxo de Repository (consultas via procedure).

Arquitetura em camadas — como explicar para a banca
REQUISIÇÃO DO USUÁRIO (frontend)
        │
        ▼
   CONTROLLER   → classe (MethodView) que recebe a requisição HTTP,
                  chama o Service certo, devolve a resposta em JSON.
                  (backend/controllers/)
        │
        ▼
    SERVICE     → representa UM caso de uso específico (ex: "criar um
                  usuário", "listar campeonatos disponíveis").
                  Não acessa o banco diretamente.
                  (backend/services/)
        │
        ▼
 ┌──────┴──────┐
 ▼             ▼
MODEL      REPOSITORY
(CRUD       (consultas
básico,     avançadas,
via ORM)    via procedure)
(models/)   (repositories/)
 │             │
 ▼             ▼
BANCO DE DADOS (MySQL)
Regra usada para decidir entre Model e Repository
CRUD simples (criar, listar, buscar por ID, atualizar, deletar um registro de UMA tabela) → fica na Model, através dos métodos herdados do CRUDMixin.
Consultas complexas (filtros com WHERE, ordenações com ORDER BY, junção de tabelas com JOIN, relatórios com agregações como COUNT) → ficam em uma procedure no banco de dados, acessada pela camada Repository.
Controllers como classes
Tanto o CRUD básico (controllers.py) quanto os relatórios (report_controller.py) usam o recurso nativo do Flask MethodView: cada Controller é uma classe, e cada método HTTP (GET, POST, PUT, DELETE) vira um método dessa classe.

Estrutura de pastas deste pacote
backend/
├── app.py                          # ponto de entrada: liga tudo
├── requirements.txt                 # bibliotecas Python necessárias
├── models/
│   ├── __init__.py                  # reexporta as Models
│   ├── db_instance.py               # instância única do SQLAlchemy
│   ├── crud_mixin.py                # métodos de CRUD reaproveitados
│   ├── usuario.py                   # Model: Usuario
│   ├── campeonato.py                # Model: Campeonato
│   ├── quadra.py                    # Model: Quadra
│   ├── inscricao.py                 # Model: Inscricao
│   ├── dupla.py                     # Model: Dupla
│   ├── partida.py                   # Model: Partida
│   └── notificacao.py               # Model: Notificacao
├── services/
│   ├── crud_services.py             # 35 classes: 5 casos de uso x 7 entidades
│   └── report_service.py            # 5 classes: casos de uso dos relatórios
├── controllers/
│   ├── controllers.py               # Controllers do CRUD (classes MethodView)
│   └── report_controller.py         # Controllers dos relatórios (classes MethodView)
├── repositories/
│   └── report_repository.py         # acesso às procedures do banco
└── database/
    └── procedures.sql               # as 5 procedures, comentadas

frontend/
└── index.html                       # tela única: CRUD + Relatórios
Todas as rotas disponíveis
CRUD básico (substitua {entidade} por: usuarios, campeonatos, quadras, inscricoes, duplas, partidas ou notificacoes):

Método	Rota	Ação
POST	/api/{entidade}	Cria um novo registro
GET	/api/{entidade}	Lista todos os registros
GET	/api/{entidade}/<id>	Busca um registro por ID
PUT	/api/{entidade}/<id>	Atualiza um registro
DELETE	/api/{entidade}/<id>	Remove um registro
Relatórios (funcionalidades avançadas, via procedures):

Funcionalidade	Procedure	Rota da API	SQL utilizado
Campeonatos disponíveis	sp_campeonatos_disponiveis	GET /api/relatorios/campeonatos-disponiveis?categoria=&nivel=	WHERE + ORDER BY
Ranking de duplas	sp_ranking_duplas	GET /api/relatorios/ranking-duplas	JOIN + COUNT + ORDER BY
Inscritos de um campeonato	sp_inscritos_campeonato	GET /api/relatorios/inscritos-campeonato/<id>	JOIN triplo
Histórico de partidas de um usuário	sp_historico_partidas_usuario	GET /api/relatorios/historico-usuario/<id>	JOIN múltiplo + CASE
Quadras mais utilizadas	sp_quadras_mais_utilizadas	GET /api/relatorios/quadras-mais-utilizadas	JOIN + COUNT + ORDER BY
Como executar o projeto do zero
1. Pré-requisitos
Python 3.10+
XAMPP (com MySQL) — apachefriends.org
2. Banco de dados
Abra o XAMPP Control Panel e clique em Start no Apache e no MySQL
Acesse http://localhost/phpmyadmin/
Crie um banco chamado ftvworld
Vá na aba SQL e cole todo o conteúdo de backend/database/procedures.sql → Executar
3. Backend
cd backend
pip install -r requirements.txt
python app.py
Se aparecer Running on http://127.0.0.1:5000 sem erros, as 7 tabelas foram criadas automaticamente no banco ftvworld.

Se o seu MySQL usa outro usuário/senha/nome de banco, ajuste a linha SQLALCHEMY_DATABASE_URI dentro de backend/app.py.

4. Frontend
Abra o arquivo frontend/index.html diretamente no navegador (o backend precisa estar rodando primeiro).

Pontos para destacar na apresentação à banca
Separação de responsabilidades clara: cada camada (Controller, Service, Model/Repository) tem uma única razão para existir.
Reuso sem duplicação: o CRUDMixin evita repetir os mesmos 5 métodos em 7 classes diferentes, mas cada Model continua sendo dona do seu próprio CRUD.
Uma classe por caso de uso: facilita adicionar regras de negócio futuras (ex: validação de e-mail duplicado) sem misturar lógica de diferentes operações.
Procedures no banco: a lógica de consultas complexas (JOIN, WHERE, ORDER BY, agregações) fica centralizada no banco de dados, sendo chamada pela camada Repository — não pelo ORM.
Controllers como classes (MethodView, recurso nativo do Flask): tanto o CRUD quanto os relatórios usam esse padrão — cada método HTTP (GET, POST, PUT, DELETE) é um método da classe.
Equipe
Davi César
Bernardo Ribeiro
Bernardo Santana
Sophia Rezende
Rhayan Prates
Pedro Temponi
