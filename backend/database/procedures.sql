-- ============================================================================
-- PROCEDURES.SQL — Funcionalidades avançadas do projeto FutWorld
-- ============================================================================
-- Este script cria 5 PROCEDURES (rotinas armazenadas) diretamente no banco
-- de dados MySQL. Uma procedure é um bloco de código SQL, com nome e
-- parâmetros, que fica salvo DENTRO do banco e pode ser chamado a
-- qualquer momento com "CALL nome_da_procedure(parametros)".
--
-- POR QUE USAR PROCEDURES?
-- A atividade exige que consultas complexas (com WHERE, JOIN, ORDER BY,
-- agregações) fiquem no banco de dados, e sejam acessadas pela camada
-- Repository do backend — não implementadas com múltiplas chamadas ao
-- ORM em Python. Isso concentra a lógica de consulta em um único lugar
-- (o banco), e separa claramente:
--   - CRUD básico  -> feito pela Model, via ORM (SQLAlchemy)
--   - Consultas complexas -> feitas pelo banco, via procedure, acessada
--     pela camada Repository
--
-- COMO USAR ESTE ARQUIVO:
-- Cole todo o conteúdo na aba "SQL" do phpMyAdmin, dentro do banco
-- "ftvworld", e execute. Isso cria as 5 procedures de uma vez.
-- ============================================================================

-- O ";" é usado tanto para separar comandos SQL comuns quanto para
-- separar comandos DENTRO de uma procedure. Por isso, trocamos
-- temporariamente o delimitador para "$$", assim o MySQL não se
-- confunde ao ler o código de dentro de cada procedure.
DELIMITER $$


-- ============================================================================
-- PROCEDURE 1: sp_campeonatos_disponiveis
-- ----------------------------------------------------------------------------
-- Retorna os campeonatos que ainda têm vagas abertas, com filtros
-- OPCIONAIS de categoria e nível, ordenados pela data mais próxima.
--
-- SQL utilizado: WHERE (filtro de status/vagas/categoria/nível) + ORDER BY
-- ============================================================================
DROP PROCEDURE IF EXISTS sp_campeonatos_disponiveis $$
CREATE PROCEDURE sp_campeonatos_disponiveis(
    IN p_categoria VARCHAR(50),  -- parâmetro de entrada: categoria (pode vir vazio/nulo)
    IN p_nivel VARCHAR(50)       -- parâmetro de entrada: nível (pode vir vazio/nulo)
)
BEGIN
    SELECT *
    FROM campeonatos
    WHERE status = 'aberto'
      AND vagas_disponiveis > 0
      -- Se o parâmetro vier vazio/nulo, ignora o filtro (mostra todas as categorias/níveis)
      AND (p_categoria IS NULL OR p_categoria = '' OR categoria = p_categoria)
      AND (p_nivel IS NULL OR p_nivel = '' OR nivel = p_nivel)
    ORDER BY data ASC;  -- campeonatos mais próximos aparecem primeiro
END $$


-- ============================================================================
-- PROCEDURE 2: sp_ranking_duplas
-- ----------------------------------------------------------------------------
-- Calcula quantas vitórias cada dupla teve em partidas finalizadas, e
-- devolve o ranking ordenado da dupla com mais vitórias para a com menos.
--
-- SQL utilizado: JOIN (duplas + usuarios + partidas) + COUNT + ORDER BY
-- ============================================================================
DROP PROCEDURE IF EXISTS sp_ranking_duplas $$
CREATE PROCEDURE sp_ranking_duplas()
BEGIN
    SELECT
        d.id AS id_dupla,
        d.categoria,
        u1.nome AS jogador1,
        u2.nome AS jogador2,

        -- Conta como vitória quando a dupla jogou como dupla1 e fez mais
        -- pontos que a dupla2 (ou o contrário, quando jogou como dupla2)
        COUNT(CASE
            WHEN (p.id_dupla1 = d.id AND p.placar_dupla1 > p.placar_dupla2)
              OR (p.id_dupla2 = d.id AND p.placar_dupla2 > p.placar_dupla1)
            THEN 1 END) AS vitorias,

        COUNT(p.id) AS partidas_jogadas

    FROM duplas d
    -- LEFT JOIN: mesmo duplas que ainda não jogaram nenhuma partida aparecem no ranking (com 0 vitórias)
    LEFT JOIN usuarios u1 ON u1.id = d.id_usuario1
    LEFT JOIN usuarios u2 ON u2.id = d.id_usuario2
    LEFT JOIN partidas p
        ON (p.id_dupla1 = d.id OR p.id_dupla2 = d.id)
       AND p.status = 'finalizada'  -- só considera partidas já concluídas
    GROUP BY d.id, d.categoria, u1.nome, u2.nome
    ORDER BY vitorias DESC;  -- do maior número de vitórias para o menor
END $$


-- ============================================================================
-- PROCEDURE 3: sp_inscritos_campeonato
-- ----------------------------------------------------------------------------
-- Lista as duplas inscritas em UM campeonato específico, já trazendo os
-- nomes dos dois jogadores de cada dupla (evita que o frontend precise
-- fazer 3 requisições separadas para montar essa informação).
--
-- SQL utilizado: JOIN triplo (inscricoes -> duplas -> usuarios)
-- ============================================================================
DROP PROCEDURE IF EXISTS sp_inscritos_campeonato $$
CREATE PROCEDURE sp_inscritos_campeonato(
    IN p_id_campeonato INT  -- qual campeonato consultar
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
    JOIN duplas d ON d.id = i.id_dupla                -- liga inscrição à dupla
    LEFT JOIN usuarios u1 ON u1.id = d.id_usuario1     -- liga dupla ao 1º jogador
    LEFT JOIN usuarios u2 ON u2.id = d.id_usuario2     -- liga dupla ao 2º jogador
    WHERE i.id_campeonato = p_id_campeonato
    ORDER BY i.data_inscricao ASC;  -- ordem de quem se inscreveu primeiro
END $$


-- ============================================================================
-- PROCEDURE 4: sp_historico_partidas_usuario
-- ----------------------------------------------------------------------------
-- Retorna todas as partidas que um usuário específico participou (através
-- de qualquer dupla que ele tenha formado), mostrando o placar do próprio
-- jogador, o placar do adversário, e o campeonato correspondente.
--
-- SQL utilizado: JOIN múltiplo + CASE (para descobrir quem foi o adversário)
-- ============================================================================
DROP PROCEDURE IF EXISTS sp_historico_partidas_usuario $$
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

        -- CASE: descobre se o usuário jogou como "dupla1" ou "dupla2" na
        -- partida, para saber qual coluna de placar é a dele e qual é do adversário
        CASE WHEN p.id_dupla1 = d_jogador.id THEN p.placar_dupla1 ELSE p.placar_dupla2 END AS placar_jogador,
        CASE WHEN p.id_dupla1 = d_jogador.id THEN p.placar_dupla2 ELSE p.placar_dupla1 END AS placar_adversario,

        d_adv.id AS id_dupla_adversaria

    FROM partidas p
    -- Encontra a dupla do usuário que participou dessa partida
    JOIN duplas d_jogador
        ON (d_jogador.id_usuario1 = p_id_usuario OR d_jogador.id_usuario2 = p_id_usuario)
       AND (p.id_dupla1 = d_jogador.id OR p.id_dupla2 = d_jogador.id)
    -- Encontra a dupla adversária (a que NÃO é a do usuário)
    LEFT JOIN duplas d_adv
        ON d_adv.id = CASE WHEN p.id_dupla1 = d_jogador.id THEN p.id_dupla2 ELSE p.id_dupla1 END
    LEFT JOIN campeonatos c ON c.id = p.id_campeonato
    ORDER BY p.data_hora DESC;  -- partidas mais recentes primeiro
END $$


-- ============================================================================
-- PROCEDURE 5: sp_quadras_mais_utilizadas
-- ----------------------------------------------------------------------------
-- Relatório simples: para cada quadra cadastrada, conta quantas partidas
-- já foram realizadas nela, ordenando da mais usada para a menos usada.
--
-- SQL utilizado: JOIN + COUNT + ORDER BY
-- ============================================================================
DROP PROCEDURE IF EXISTS sp_quadras_mais_utilizadas $$
CREATE PROCEDURE sp_quadras_mais_utilizadas()
BEGIN
    SELECT
        q.id AS id_quadra,
        q.nome,
        q.cidade,
        COUNT(p.id) AS total_partidas
    FROM quadras q
    -- LEFT JOIN: quadras que nunca sediaram uma partida também aparecem (com 0)
    LEFT JOIN partidas p ON p.id_quadra = q.id
    GROUP BY q.id, q.nome, q.cidade
    ORDER BY total_partidas DESC;
END $$

-- Devolve o delimitador ao normal (";"), para que o restante de
-- comandos SQL do banco volte a funcionar normalmente.
DELIMITER ;
