# ============================================================================
# CONTROLLERS.PY
# ============================================================================
# CAMADA CONTROLLER: responsável por RECEBER as requisições HTTP da API,
# repassar para o Service correto, e devolver a resposta em formato JSON.
#
# Aqui, as Controllers são CLASSES de verdade, usando o recurso nativo
# do Flask chamado "MethodView" (flask.views.MethodView). Cada método
# HTTP (GET, POST, PUT, DELETE) vira um método da classe.
#
# Para evitar repetir a mesma lógica 7 vezes (uma por entidade), criamos
# uma classe BASE (CRUDController) com toda a lógica genérica de
# requisição/resposta. Cada entidade então cria uma SUBCLASSE que só
# precisa dizer QUAIS Services específicos ela deve usar.
# ============================================================================
from flask import request, jsonify
from flask.views import MethodView

from services.crud_services import (
    CreateUsuarioService, ListUsuarioService, FindUsuarioByIdService, UpdateUsuarioService, DeleteUsuarioService,
    CreateCampeonatoService, ListCampeonatoService, FindCampeonatoByIdService, UpdateCampeonatoService, DeleteCampeonatoService,
    CreateQuadraService, ListQuadraService, FindQuadraByIdService, UpdateQuadraService, DeleteQuadraService,
    CreateInscricaoService, ListInscricaoService, FindInscricaoByIdService, UpdateInscricaoService, DeleteInscricaoService,
    CreateDuplaService, ListDuplaService, FindDuplaByIdService, UpdateDuplaService, DeleteDuplaService,
    CreatePartidaService, ListPartidaService, FindPartidaByIdService, UpdatePartidaService, DeletePartidaService,
    CreateNotificacaoService, ListNotificacaoService, FindNotificacaoByIdService, UpdateNotificacaoService, DeleteNotificacaoService,
)


class CRUDController(MethodView):
    """
    Controller BASE, genérica. Contém toda a lógica de "traduzir" uma
    requisição HTTP em uma chamada ao Service certo, e devolver a
    resposta em JSON.

    As subclasses (uma por entidade, abaixo) só precisam apontar QUAIS
    classes de Service usar — elas não reescrevem nenhuma lógica.
    """
    create_service = None   # será sobrescrito em cada subclasse
    list_service = None
    find_service = None
    update_service = None
    delete_service = None

    def get(self, id=None):
        """
        Trata requisições GET.
        - Se "id" não foi informado na URL -> lista todos os registros.
        - Se "id" foi informado -> busca apenas aquele registro.
        """
        if id is None:
            registros = self.list_service.execute()
            return jsonify([r.to_dict() for r in registros]), 200

        registro = self.find_service.execute(id)
        if not registro:
            return jsonify({"error": "Registro não encontrado"}), 404
        return jsonify(registro.to_dict()), 200

    def post(self):
        """Trata requisições POST: cria um novo registro a partir do JSON enviado."""
        dados = request.get_json()
        try:
            registro = self.create_service.execute(dados)
            return jsonify(registro.to_dict()), 201  # 201 = "Created"
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def put(self, id):
        """Trata requisições PUT: atualiza um registro existente."""
        dados = request.get_json()
        try:
            registro = self.update_service.execute(id, dados)
            if not registro:
                return jsonify({"error": "Registro não encontrado"}), 404
            return jsonify(registro.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def delete(self, id):
        """Trata requisições DELETE: remove um registro existente."""
        sucesso = self.delete_service.execute(id)
        if not sucesso:
            return jsonify({"error": "Registro não encontrado"}), 404
        return '', 204  # 204 = "sem conteúdo", indicando sucesso na exclusão


# ============================================================================
# Uma classe de Controller PARA CADA entidade. Cada uma só declara quais
# Services usar — a lógica de verdade está toda na classe base acima.
# ============================================================================

class UsuarioController(CRUDController):
    create_service = CreateUsuarioService
    list_service = ListUsuarioService
    find_service = FindUsuarioByIdService
    update_service = UpdateUsuarioService
    delete_service = DeleteUsuarioService


class CampeonatoController(CRUDController):
    create_service = CreateCampeonatoService
    list_service = ListCampeonatoService
    find_service = FindCampeonatoByIdService
    update_service = UpdateCampeonatoService
    delete_service = DeleteCampeonatoService


class QuadraController(CRUDController):
    create_service = CreateQuadraService
    list_service = ListQuadraService
    find_service = FindQuadraByIdService
    update_service = UpdateQuadraService
    delete_service = DeleteQuadraService


class InscricaoController(CRUDController):
    create_service = CreateInscricaoService
    list_service = ListInscricaoService
    find_service = FindInscricaoByIdService
    update_service = UpdateInscricaoService
    delete_service = DeleteInscricaoService


class DuplaController(CRUDController):
    create_service = CreateDuplaService
    list_service = ListDuplaService
    find_service = FindDuplaByIdService
    update_service = UpdateDuplaService
    delete_service = DeleteDuplaService


class PartidaController(CRUDController):
    create_service = CreatePartidaService
    list_service = ListPartidaService
    find_service = FindPartidaByIdService
    update_service = UpdatePartidaService
    delete_service = DeletePartidaService


class NotificacaoController(CRUDController):
    create_service = CreateNotificacaoService
    list_service = ListNotificacaoService
    find_service = FindNotificacaoByIdService
    update_service = UpdateNotificacaoService
    delete_service = DeleteNotificacaoService


def registrar_rotas_crud(app):
    """
    Registra, no aplicativo Flask, as rotas de todas as 7 entidades.

    Para cada entidade, cria duas rotas:
      /api/<entidade>          -> GET (listar) e POST (criar)
      /api/<entidade>/<id>     -> GET (buscar um), PUT (atualizar), DELETE (remover)

    Esta função é chamada uma única vez, dentro do app.py.
    """
    entidades = [
        ('usuarios', UsuarioController),
        ('campeonatos', CampeonatoController),
        ('quadras', QuadraController),
        ('inscricoes', InscricaoController),
        ('duplas', DuplaController),
        ('partidas', PartidaController),
        ('notificacoes', NotificacaoController),
    ]

    for nome, controller_class in entidades:
        view = controller_class.as_view(nome)  # transforma a classe em uma "view" do Flask
        app.add_url_rule(f'/api/{nome}', view_func=view, methods=['GET', 'POST'])
        app.add_url_rule(f'/api/{nome}/<int:id>', view_func=view, methods=['GET', 'PUT', 'DELETE'])
