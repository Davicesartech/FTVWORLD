# ============================================================================
# REPORT_REPOSITORY.PY
# ============================================================================
# CAMADA REPOSITORY: responsável por ENCAPSULAR o acesso a consultas
# complexas do banco de dados.
#
# Diferente do CRUD básico (que usa o ORM SQLAlchemy através da Model),
# aqui o acesso é feito chamando diretamente as PROCEDURES criadas no
# banco MySQL (usando "CALL nome_da_procedure(...)"). Isso é necessário
# porque a lógica de JOIN, WHERE, ORDER BY e agregações (COUNT, etc.)
# está escrita em SQL dentro do banco, não em Python.
#
# Por que fazer assim, e não usar o ORM para essas consultas também?
# Porque a atividade pede explicitamente que funcionalidades com filtros,
# buscas, ordenações, relatórios e combinações entre tabelas sejam
# implementadas via PROCEDURES no banco, acessadas pela camada Repository.
# ============================================================================

from datetime import date, datetime, time, timedelta
from decimal import Decimal
from models import db


def _serialize_value(v):
    """
    Converte tipos de dado que o formato JSON não entende nativamente
    (datas, horários, números decimais) em algo que pode ser enviado
    como resposta da API.
    """
    if isinstance(v, (datetime, date, time)):
        return v.isoformat()
    # Colunas do tipo TIME do MySQL chegam pelo PyMySQL como timedelta
    # (não como datetime.time), então precisam de um tratamento à parte
    # antes de virar JSON. Convertemos para o formato "HH:MM:SS".
    if isinstance(v, timedelta):
        total_seconds = int(v.total_seconds())
        horas, resto = divmod(total_seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    if isinstance(v, Decimal):
        return float(v)
    return v


def _serialize_row(row_dict):
    """Aplica a conversão acima em todos os campos de uma linha de resultado."""
    return {k: _serialize_value(v) for k, v in row_dict.items()}


class ReportRepository:
    """
    Repository responsável por todas as consultas avançadas do projeto,
    feitas através de procedures no banco MySQL.
    """

    @staticmethod
    def _call_procedure(proc_name, params=None):
        """
        Método auxiliar genérico: abre uma conexão "crua" com o banco
        (fora do ORM), executa "CALL nome_da_procedure(parametros)",
        e devolve o resultado já convertido em uma lista de dicionários
        (um dicionário por linha retornada).
        """
        params = params or []
        connection = db.engine.raw_connection()  # conexão direta, sem passar pelo ORM
        try:
            cursor = connection.cursor()
            cursor.callproc(proc_name, params)  # executa a procedure com os parâmetros

            # Descobre os nomes das colunas retornadas pela procedure
            columns = [col[0] for col in cursor.description] if cursor.description else []
            rows = cursor.fetchall()

            # Transforma cada linha (tupla) em um dicionário {coluna: valor}
            result = [_serialize_row(dict(zip(columns, row))) for row in rows]

            cursor.close()
            connection.commit()
            return result
        finally:
            connection.close()  # sempre fecha a conexão, mesmo se der erro

    # ------------------------------------------------------------------
    # Cada método abaixo corresponde a UMA das 5 procedures criadas no
    # banco (arquivo backend/database/procedures.sql)
    # ------------------------------------------------------------------

    @staticmethod
    def campeonatos_disponiveis(categoria=None, nivel=None):
        """Chama sp_campeonatos_disponiveis: WHERE (status/vagas) + filtros + ORDER BY data."""
        return ReportRepository._call_procedure(
            'sp_campeonatos_disponiveis', [categoria, nivel]
        )

    @staticmethod
    def ranking_duplas():
        """Chama sp_ranking_duplas: JOIN entre duplas/usuarios/partidas + COUNT + ORDER BY."""
        return ReportRepository._call_procedure('sp_ranking_duplas', [])

    @staticmethod
    def inscritos_campeonato(id_campeonato):
        """Chama sp_inscritos_campeonato: JOIN triplo (inscricoes -> duplas -> usuarios)."""
        return ReportRepository._call_procedure(
            'sp_inscritos_campeonato', [id_campeonato]
        )

    @staticmethod
    def historico_partidas_usuario(id_usuario):
        """Chama sp_historico_partidas_usuario: JOIN múltiplo + CASE para achar o adversário."""
        return ReportRepository._call_procedure(
            'sp_historico_partidas_usuario', [id_usuario]
        )

    @staticmethod
    def quadras_mais_utilizadas():
        """Chama sp_quadras_mais_utilizadas: JOIN + COUNT + ORDER BY."""
        return ReportRepository._call_procedure('sp_quadras_mais_utilizadas', [])
