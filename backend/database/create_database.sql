-- create_database.sql
-- Script de criação do banco de dados do projeto FutWorld (MySQL)
-- Observação: a aplicação Flask (via SQLAlchemy) também consegue criar essas tabelas
-- automaticamente ao rodar "python app.py" (db.create_all()).
-- Este script serve como referência/registro da estrutura do banco, conforme exigido na entrega.
-- As chaves estrangeiras (id_*) estão como colunas simples (sem constraint FK),
-- pois as relações da modelagem ainda serão corrigidas pelo grupo.

CREATE DATABASE IF NOT EXISTS ftvworld;
USE ftvworld;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    nivel VARCHAR(50),
    cidade VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS campeonatos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    data DATE,
    horario TIME,
    categoria VARCHAR(50),
    nivel VARCHAR(50),
    vagas_total INT,
    vagas_disponiveis INT,
    status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS quadras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    numero_quadras INT,
    contato VARCHAR(50),
    id_responsavel INT
);

CREATE TABLE IF NOT EXISTS inscricoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(50),
    data_inscricao DATE,
    id_campeonato INT,
    id_dupla INT
);

CREATE TABLE IF NOT EXISTS duplas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario1 INT,
    id_usuario2 INT,
    categoria VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS partidas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    fase VARCHAR(50),
    placar_dupla1 INT DEFAULT 0,
    placar_dupla2 INT DEFAULT 0,
    data_hora DATETIME,
    status VARCHAR(50),
    id_campeonato INT,
    id_dupla1 INT,
    id_dupla2 INT,
    id_quadra INT
);

CREATE TABLE IF NOT EXISTS notificacoes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mensagem VARCHAR(255) NOT NULL,
    lida BOOLEAN DEFAULT 0,
    data_envio DATE,
    id_usuario INT
);

-- ============================================================
-- PROCEDURES
-- As 5 procedures abaixo (sp_campeonatos_disponiveis, sp_ranking_duplas,
-- sp_inscritos_campeonato, sp_historico_partidas_usuario,
-- sp_quadras_mais_utilizadas) já foram criadas diretamente no banco
-- via phpMyAdmin. Substitua este bloco pelo SQL real de cada uma
-- (Exportar -> copiar o CREATE PROCEDURE de cada uma no phpMyAdmin)
-- para que o script fique completo e reproduzível do zero.
-- ============================================================
