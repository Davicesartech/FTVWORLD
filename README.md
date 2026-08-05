# FTVWorld - Sistema de Gestão Esportiva

Projeto acadêmico desenvolvido pela equipe **FTV WORLD** para a disciplina **Projeto de Software**.

Sistema de gestão de campeonatos esportivos com CRUD completo (Backend em Flask + Frontend em HTML/CSS/JS) e um módulo de **Relatórios** com consultas complexas implementadas via **stored procedures** no MySQL.

## Estrutura do repositório

```
projeto/
├── frontend/
│   └── index.html
└── backend/
    ├── controllers/
    │   ├── controllers.py          (CRUD genérico)
    │   └── report_controller.py    (rotas de relatórios)
    ├── models/
    │   └── models.py
    ├── repositories/
    │   └── report_repository.py    (acesso às procedures)
    ├── services/
    │   ├── crud_service.py         (casos de uso do CRUD)
    │   └── report_service.py       (casos de uso dos relatórios)
    ├── database/
    │   └── create_database.sql
    ├── app.py
    └── requirements.txt
```

- **frontend/**: interface única e dinâmica (HTML + Tailwind + JS puro), com duas seções alternáveis: **CRUD** (gerencia as 7 entidades) e **Relatórios** (consome as 5 funcionalidades avançadas).
- **backend/**: API Web em Flask.
  - **controllers/**: recebem as requisições da API e retornam as respostas (rotas REST).
  - **services/**: implementam os casos de uso, separados por finalidade (CRUD básico x relatórios).
  - **models/**: representam as entidades do domínio e o mapeamento com o banco (SQLAlchemy) — usadas pelo CRUD básico.
  - **repositories/**: encapsulam o acesso a consultas complexas do banco, feitas via **stored procedures** no MySQL (`report_repository.py` chama as procedures com `cursor.callproc(...)` em vez de usar o ORM).
  - **database/**: script de criação do banco (`create_database.sql`), incluindo as tabelas e as procedures.

## Banco de dados

Migrado de SQLite para **MySQL**. String de conexão em `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ftvworld'
```

> ⚠️ Se seu MySQL local usa outro usuário/senha, ajuste essa linha antes de rodar o projeto.

## Models implementadas (CRUD básico)

| Model         | Descrição                                       |
| ------------- | ----------------------------------------------- |
| `Usuario`     | Usuários do sistema (jogadores, gestores, etc.) |
| `Campeonato`  | Campeonatos cadastrados                         |
| `Quadra`      | Quadras esportivas disponíveis                  |
| `Inscricao`   | Inscrições de duplas em campeonatos             |
| `Dupla`       | Duplas formadas por usuários                    |
| `Partida`     | Partidas de um campeonato                       |
| `Notificacao` | Notificações enviadas aos usuários              |

> ⚠️ As relações entre as tabelas (chaves estrangeiras) foram implementadas como colunas simples (`id_*`), sem constraints de integridade, pois a modelagem de domínio original ainda será corrigida pelo grupo.

## Rotas de CRUD básico

Todas as entidades acima possuem o mesmo padrão de rotas REST (substitua `{entidade}` por: `usuarios`, `campeonatos`, `quadras`, `inscricoes`, `duplas`, `partidas` ou `notificacoes`):

| Método | Rota                   | Ação                     |
| ------ | ---------------------- | ------------------------ |
| POST   | `/api/{entidade}`      | Cria um novo registro    |
| GET    | `/api/{entidade}`      | Lista todos os registros |
| GET    | `/api/{entidade}/{id}` | Busca um registro por ID |
| PUT    | `/api/{entidade}/{id}` | Atualiza um registro     |
| DELETE | `/api/{entidade}/{id}` | Remove um registro       |

## Funcionalidades avançadas (Repository + Procedures)

Estas 5 funcionalidades vão além do CRUD básico: envolvem filtros, ordenações, `JOIN`/agregações entre tabelas, implementadas como **procedures no MySQL** e acessadas pela camada **Repository** (`report_repository.py`), sem passar pelo ORM.

| # | Funcionalidade | Procedure | Rota | Service |
|---|---|---|---|---|
| 1 | Campeonatos disponíveis, com filtro opcional por categoria e nível | `sp_campeonatos_disponiveis` | `GET /api/relatorios/campeonatos-disponiveis?categoria=&nivel=` | `CampeonatosDisponiveisService` |
| 2 | Ranking de duplas por número de vitórias | `sp_ranking_duplas` | `GET /api/relatorios/ranking-duplas` | `RankingDuplasService` |
| 3 | Jogadores inscritos em um campeonato específico | `sp_inscritos_campeonato` | `GET /api/relatorios/inscritos-campeonato/<id_campeonato>` | `InscritosCampeonatoService` |
| 4 | Histórico de partidas de um usuário (adversário e placar) | `sp_historico_partidas_usuario` | `GET /api/relatorios/historico-usuario/<id_usuario>` | `HistoricoPartidasUsuarioService` |
| 5 | Quantidade de partidas realizadas por quadra | `sp_quadras_mais_utilizadas` | `GET /api/relatorios/quadras-mais-utilizadas` | `QuadrasMaisUtilizadasService` |

Fluxo de cada requisição: **Controller** (`report_controller.py`) recebe a rota → chama o **Service** correspondente (`report_service.py`, um caso de uso por classe) → o Service chama o **Repository** (`report_repository.py`) → o Repository executa a procedure no MySQL via `cursor.callproc(...)` e devolve os dados já serializados em JSON.

## Frontend

O `frontend/index.html` tem um alternador **CRUD / Relatórios** no topo:
- **CRUD**: mesmo comportamento de antes — seletor de entidade, tabela e modal de criação/edição.
- **Relatórios**: seletor com as 5 funcionalidades acima. Ao escolher uma, os campos de filtro necessários aparecem (ex: "ID do Campeonato" para o relatório de inscritos). O botão "Buscar" chama a rota correspondente e monta a tabela de resultado dinamicamente, a partir das colunas retornadas pela procedure.

## Como executar o projeto

### Banco de dados (MySQL)

1. Crie o banco `ftvworld` (ou deixe o `create_database.sql` criar):
   ```
   mysql -u root -p < backend/database/create_database.sql
   ```
2. As 5 procedures também precisam existir no banco `ftvworld` (crie-as via phpMyAdmin ou incluindo o SQL delas no mesmo script).

### Backend (API Flask)

1. Entre na pasta do backend:
   ```
   cd backend
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Confira a string de conexão MySQL em `app.py` e ajuste usuário/senha se necessário.
5. Execute a aplicação:
   ```
   python app.py
   ```
6. A API estará disponível em `http://127.0.0.1:5000`.

### Frontend

1. Com o backend rodando, basta abrir o arquivo `frontend/index.html` diretamente no navegador.
2. Não é necessário nenhum servidor adicional — o frontend faz as requisições diretamente para `http://127.0.0.1:5000/api`.

## Equipe

- Davi César
- Bernardo Ribeiro
- Bernardo Santana
- Sophia Rezende
- Rhayan Prates
- Pedro Temponi
