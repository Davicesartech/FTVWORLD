# ============================================================================
# REPORT_SERVICE.PY
# ============================================================================
# Services das 5 FUNCIONALIDADES AVANÇADAS do projeto (consultas com
# filtros, JOIN, ORDER BY e agregações, implementadas via procedures
# no banco de dados).
#
# Assim como no crud_services.py, cada classe representa um único caso
# de uso. A diferença é que, aqui, o Service delega o trabalho para o
# REPOSITORY (não para a Model), porque a lógica dessas consultas é
# complexa demais para viver dentro da Model — ela foi escrita como
# uma procedure diretamente no banco MySQL, e o Repository é a camada
# responsável por chamar essa procedure.
# ============================================================================
from repositories.report_repository import ReportRepository


class CampeonatosDisponiveisService:
    """Caso de uso: listar campeonatos com vagas disponíveis, com filtros opcionais."""
    @staticmethod
    def execute(categoria=None, nivel=None):
        return ReportRepository.campeonatos_disponiveis(categoria, nivel)


class RankingDuplasService:
    """Caso de uso: ranking de duplas por número de vitórias."""
    @staticmethod
    def execute():
        return ReportRepository.ranking_duplas()


class InscritosCampeonatoService:
    """Caso de uso: listar os jogadores inscritos em um campeonato específico."""
    @staticmethod
    def execute(id_campeonato):
        return ReportRepository.inscritos_campeonato(id_campeonato)


class HistoricoPartidasUsuarioService:
    """Caso de uso: histórico de partidas de um usuário, com adversário e placar."""
    @staticmethod
    def execute(id_usuario):
        return ReportRepository.historico_partidas_usuario(id_usuario)


class QuadrasMaisUtilizadasService:
    """Caso de uso: relatório de quantidade de partidas por quadra."""
    @staticmethod
    def execute():
        return ReportRepository.quadras_mais_utilizadas()
