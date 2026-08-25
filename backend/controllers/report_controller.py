# ============================================================================
# REPORT_CONTROLLER.PY
# ============================================================================
# Controller das 5 rotas de RELATÓRIOS (funcionalidades avançadas).
#
# Assim como em controllers.py, cada Controller aqui é uma CLASSE que usa
# o recurso nativo do Flask "MethodView" (flask.views.MethodView). Cada
# classe representa um recurso da API, e o método HTTP correspondente
# (aqui, sempre GET) vira um método da classe.
#
# Diferente do CRUD básico (uma única classe base reaproveitada 7 vezes),
# cada relatório tem parâmetros e regras de leitura diferentes entre si
# (alguns recebem filtros via query string, outros recebem um ID na URL,
# outros não recebem nada) — por isso cada um tem sua própria classe,
# mas todas seguem o mesmo papel: ler os parâmetros da requisição, chamar
# o Service correspondente, e devolver o resultado em JSON.
# ============================================================================
from flask import request, jsonify
from flask.views import MethodView

from services.report_service import (
    CampeonatosDisponiveisService,
    RankingDuplasService,
    InscritosCampeonatoService,
    HistoricoPartidasUsuarioService,
    QuadrasMaisUtilizadasService,
)


class CampeonatosDisponiveisController(MethodView):
    """
    GET /api/relatorios/campeonatos-disponiveis?categoria=X&nivel=Y
    Os filtros de categoria e nível são opcionais (via query string).
    """
    def get(self):
        try:
            categoria = request.args.get('categoria') or None
            nivel = request.args.get('nivel') or None
            data = CampeonatosDisponiveisService.execute(categoria, nivel)
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


class RankingDuplasController(MethodView):
    """GET /api/relatorios/ranking-duplas — sem parâmetros."""
    def get(self):
        try:
            data = RankingDuplasService.execute()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


class InscritosCampeonatoController(MethodView):
    """GET /api/relatorios/inscritos-campeonato/<id_campeonato>"""
    def get(self, id_campeonato):
        try:
            data = InscritosCampeonatoService.execute(id_campeonato)
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


class HistoricoUsuarioController(MethodView):
    """GET /api/relatorios/historico-usuario/<id_usuario>"""
    def get(self, id_usuario):
        try:
            data = HistoricoPartidasUsuarioService.execute(id_usuario)
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


class QuadrasMaisUtilizadasController(MethodView):
    """GET /api/relatorios/quadras-mais-utilizadas — sem parâmetros."""
    def get(self):
        try:
            data = QuadrasMaisUtilizadasService.execute()
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


def registrar_rotas_relatorios(app):
    """
    Registra, no aplicativo Flask, as 5 rotas de relatórios — cada uma
    apontando para a Controller (classe) correspondente.

    Esta função é chamada uma única vez, dentro do app.py, no lugar do
    antigo "app.register_blueprint(report_bp)".
    """
    app.add_url_rule(
        '/api/relatorios/campeonatos-disponiveis',
        view_func=CampeonatosDisponiveisController.as_view('campeonatos_disponiveis'),
        methods=['GET'],
    )
    app.add_url_rule(
        '/api/relatorios/ranking-duplas',
        view_func=RankingDuplasController.as_view('ranking_duplas'),
        methods=['GET'],
    )
    app.add_url_rule(
        '/api/relatorios/inscritos-campeonato/<int:id_campeonato>',
        view_func=InscritosCampeonatoController.as_view('inscritos_campeonato'),
        methods=['GET'],
    )
    app.add_url_rule(
        '/api/relatorios/historico-usuario/<int:id_usuario>',
        view_func=HistoricoUsuarioController.as_view('historico_usuario'),
        methods=['GET'],
    )
    app.add_url_rule(
        '/api/relatorios/quadras-mais-utilizadas',
        view_func=QuadrasMaisUtilizadasController.as_view('quadras_mais_utilizadas'),
        methods=['GET'],
    )
