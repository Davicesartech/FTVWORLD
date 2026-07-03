# FTVWorld - Sistema de Gestão Esportiva     
  Projeto acadêmico desenvolvido pela equipe **FTV WORLD** para a disciplina **Projeto de Software**.

Sistema de gestão de campeonatos esportivos com CRUD completo (Backend em Flask + Frontend em HTML/CSS/JS).

## Estrutura do repositório

```
projeto/
├── frontend/
│   └── index.html
└── backend/
    ├── controllers/
    │   └── controllers.py
    ├── models/
    │   └── models.py
    ├── repositories/
    ├── services/
    │   └── crud_service.py
    ├── database/
    │   └── create_database.sql
    ├── app.py
    └── requirements.txt
```

- **frontend/**: interface única e dinâmica (HTML + Tailwind + JS puro) que consome a API para todas as entidades.
- **backend/**: API Web em Flask.
  - **controllers/**: recebem as requisições da API e retornam as respostas (rotas REST).
  - **services/**: implementam os casos de uso (Create, List, FindById, Update, Delete).
  - **models/**: representam as entidades e o mapeamento com o banco de dados (SQLAlchemy).
  - **repositories/**: reservado para consultas mais específicas (ainda não utilizado nesta entrega, pois o CRUD básico cobriu as necessidades atuais).
  - **database/**: script de criação do banco de dados (`create_database.sql`).

## Models implementadas

| Model | Descrição |
|---|---|
| `Usuario` | Usuários do sistema (jogadores, gestores, etc.) |
| `Campeonato` | Campeonatos cadastrados |
| `Quadra` | Quadras esportivas disponíveis |
| `Inscricao` | Inscrições de duplas em campeonatos |
| `Dupla` | Duplas formadas por usuários |
| `Partida` | Partidas de um campeonato |
| `Notificacao` | Notificações enviadas aos usuários |

> ⚠️ As relações entre as tabelas (chaves estrangeiras) foram implementadas como colunas simples (`id_*`), sem constraints de integridade, pois a modelagem de domínio original ainda será corrigida pelo grupo.

## Rotas implementadas

Todas as entidades acima possuem o mesmo padrão de rotas REST (substitua `{entidade}` por: `usuarios`, `campeonatos`, `quadras`, `inscricoes`, `duplas`, `partidas` ou `notificacoes`):

| Método | Rota | Ação |
|---|---|---|
| POST | `/api/{entidade}` | Cria um novo registro |
| GET | `/api/{entidade}` | Lista todos os registros |
| GET | `/api/{entidade}/{id}` | Busca um registro por ID |
| PUT | `/api/{entidade}/{id}` | Atualiza um registro |
| DELETE | `/api/{entidade}/{id}` | Remove um registro |

## Funcionalidades implementadas

- CRUD completo (criar, listar, buscar, atualizar, deletar) para as 7 entidades do sistema, tanto no backend (API) quanto no frontend (telas).
- Frontend único e dinâmico: um seletor no topo troca a entidade sendo gerenciada, sem precisar de uma página por entidade.
- Validação e conversão automática de tipos de data/hora entre o frontend e o backend.

## Como executar o projeto

### Backend (API Flask)

1. Entre na pasta do backend:
   ```bash
   cd backend
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute a aplicação:
   ```bash
   python app.py
   ```
5. A API estará disponível em `http://127.0.0.1:5000`. O banco SQLite (`futworld.db`) é criado automaticamente dentro de `backend/database/` na primeira execução.

### Frontend

1. Com o backend rodando, basta abrir o arquivo `frontend/index.html` diretamente no navegador (duplo clique ou clique com o botão direito → "Abrir com" o navegador).
2. Não é necessário nenhum servidor adicional — o frontend faz as requisições diretamente para `http://127.0.0.1:5000/api`.

## Equipe

   - Davi César
   - Bernardo Ribeiro
   - Bernardo Santana
   - Sophia Gomes
   - Rhayan Prates
   - Pedro Temponi