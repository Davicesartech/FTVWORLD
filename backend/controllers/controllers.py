from flask import Blueprint, request, jsonify
from services.crud_service import CreateService, ListService, FindByIdService, UpdateService, DeleteService
from models.models import Usuario, Campeonato, Quadra, Inscricao, Dupla, Partida, Notificacao

def create_crud_blueprint(name, model_class):
    bp = Blueprint(name, __name__, url_prefix=f'/api/{name}')

    @bp.route('', methods=['POST'])
    def create():
        try:
            data = request.json
            obj = CreateService.execute(model_class, data)
            return jsonify(obj.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @bp.route('', methods=['GET'])
    def list_all():
        objs = ListService.execute(model_class)
        return jsonify([o.to_dict() for o in objs]), 200

    @bp.route('/<int:id>', methods=['GET'])
    def get_by_id(id):
        obj = FindByIdService.execute(model_class, id)
        return jsonify(obj.to_dict()), 200

    @bp.route('/<int:id>', methods=['PUT'])
    def update(id):
        try:
            data = request.json
            obj = UpdateService.execute(model_class, id, data)
            return jsonify(obj.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @bp.route('/<int:id>', methods=['DELETE'])
    def delete(id):
        DeleteService.execute(model_class, id)
        return jsonify({"message": f"{model_class.__name__} removido com sucesso"}), 200

    return bp
