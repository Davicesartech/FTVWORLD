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
-- ============================================================
-- PROCEDURES
-- ============================================================

DELIMITER $$

CREATE PROCEDURE sp_campeonatos_disponiveis(
    IN p_categoria VARCHAR(50),
    IN p_nivel VARCHAR(50)
)
BEGIN
    SELECT *
    FROM campeonatos
    WHERE status = 'aberto'
      AND vagas_disponiveis > 0
      AND (p_categoria IS NULL OR p_categoria = '' OR categoria = p_categoria)
      AND (p_nivel IS NULL OR p_nivel = '' OR nivel = p_nivel)
    ORDER BY data ASC;
END$$

CREATE PROCEDURE sp_ranking_duplas()
BEGIN
    SELECT
        d.id AS id_dupla,
        d.categoria,
        u1.nome AS jogador1,
        u2.nome AS jogador2,
        COUNT(CASE
            WHEN (p.id_dupla1 = d.id AND p.placar_dupla1 > p.placar_dupla2)
              OR (p.id_dupla2 = d.id AND p.placar_dupla2 > p.placar_dupla1)
            THEN 1 END) AS vitorias,
        COUNT(p.id) AS partidas_jogadas
    FROM duplas d
    LEFT JOIN usuarios u1 ON u1.id = d.id_usuario1
    LEFT JOIN usuarios u2 ON u2.id = d.id_usuario2
    LEFT JOIN partidas p
        ON (p.id_dupla1 = d.id OR p.id_dupla2 = d.id)
       AND p.status = 'finalizada'
    GROUP BY d.id, d.categoria, u1.nome, u2.nome
    ORDER BY vitorias DESC;
END$$

CREATE PROCEDURE sp_inscritos_campeonato(
    IN p_id_campeonato INT
)
BEGIN
    SELECT
        i.id AS id_inscricao,
        i.status AS status_inscricao,
        i.data_inscricao,
        d.id AS id_dupla,
        d.categoria,
        u1.nome AS jogador1,
        u2.nome AS jogador2
    FROM inscricoes i
    JOIN duplas d ON d.id = i.id_dupla
    LEFT JOIN usuarios u1 ON u1.id = d.id_usuario1
    LEFT JOIN usuarios u2 ON u2.id = d.id_usuario2
    WHERE i.id_campeonato = p_id_campeonato
    ORDER BY i.data_inscricao ASC;
END$$

CREATE PROCEDURE sp_historico_partidas_usuario(
    IN p_id_usuario INT
)
BEGIN
    SELECT
        p.id AS id_partida,
        p.fase,
        p.data_hora,
        p.status,
        c.nome AS campeonato,
        CASE WHEN p.id_dupla1 = d_jogador.id THEN p.placar_dupla1 ELSE p.placar_dupla2 END AS placar_jogador,
        CASE WHEN p.id_dupla1 = d_jogador.id THEN p.placar_dupla2 ELSE p.placar_dupla1 END AS placar_adversario,
        d_adv.id AS id_dupla_adversaria
    FROM partidas p
    JOIN duplas d_jogador
        ON (d_jogador.id_usuario1 = p_id_usuario OR d_jogador.id_usuario2 = p_id_usuario)
       AND (p.id_dupla1 = d_jogador.id OR p.id_dupla2 = d_jogador.id)
    LEFT JOIN duplas d_adv
        ON d_adv.id = CASE WHEN p.id_dupla1 = d_jogador.id THEN p.id_dupla2 ELSE p.id_dupla1 END
    LEFT JOIN campeonatos c ON c.id = p.id_campeonato
    ORDER BY p.data_hora DESC;
END$$

CREATE PROCEDURE sp_quadras_mais_utilizadas()
BEGIN
    SELECT
        q.id AS id_quadra,
        q.nome,
        q.cidade,
        COUNT(p.id) AS total_partidas
    FROM quadras q
    LEFT JOIN partidas p ON p.id_quadra = q.id
    GROUP BY q.id, q.nome, q.cidade
    ORDER BY total_partidas DESC;
END$$

DELIMITER ;
