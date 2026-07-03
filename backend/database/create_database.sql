i-- create_database.sql
-- Script de criação do banco de dados do projeto FutWorld
-- Observação: a aplicação Flask (via SQLAlchemy) cria essas tabelas automaticamente
-- ao rodar "python app.py" (banco SQLite em backend/database/futworld.db).
-- Este script serve como referência/registro da estrutura do banco, conforme exigido na entrega.
-- As chaves estrangeiras (id_*) estão como colunas simples (sem constraint FK),
-- pois as relações da modelagem ainda serão corrigidas pelo grupo.

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    nivel VARCHAR(50),
    cidade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS campeonatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    data DATE,
    horario TIME,
    categoria VARCHAR(50),
    nivel VARCHAR(50),
    vagas_total INTEGER,
    vagas_disponiveis INTEGER,
    status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS quadras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(150) NOT NULL,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    numero_quadras INTEGER,
    contato VARCHAR(50),
    id_responsavel INTEGER
);

CREATE TABLE IF NOT EXISTS inscricoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status VARCHAR(50),
    data_inscricao DATE,
    id_campeonato INTEGER,
    id_dupla INTEGER
);

CREATE TABLE IF NOT EXISTS duplas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario1 INTEGER,
    id_usuario2 INTEGER,
    categoria VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS partidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fase VARCHAR(50),
    placar_dupla1 INTEGER DEFAULT 0,
    placar_dupla2 INTEGER DEFAULT 0,
    data_hora DATETIME,
    status VARCHAR(50),
    id_campeonato INTEGER,
    id_dupla1 INTEGER
);

CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mensagem VARCHAR(255) NOT NULL,
    lida BOOLEAN DEFAULT 0,
    data_envio DATE,
    id_usuario INTEGER
);
