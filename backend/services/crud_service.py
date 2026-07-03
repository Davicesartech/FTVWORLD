from models.models import db
from datetime import datetime, time

class CreateService:
    @staticmethod
    def execute(model_class, data):
        if 'data' in data and isinstance(data['data'], str):
            data['data'] = datetime.strptime(data['data'], '%Y-%m-%d').date()
        if 'data_inscricao' in data and isinstance(data['data_inscricao'], str):
            data['data_inscricao'] = datetime.strptime(data['data_inscricao'], '%Y-%m-%d').date()
        if 'data_envio' in data and isinstance(data['data_envio'], str):
            data['data_envio'] = datetime.strptime(data['data_envio'], '%Y-%m-%d').date()
        if 'horario' in data and isinstance(data['horario'], str):
            data['horario'] = datetime.strptime(data['horario'], '%H:%M').time()
        if 'data_hora' in data and isinstance(data['data_hora'], str):
            data['data_hora'] = datetime.strptime(data['data_hora'], '%Y-%m-%dT%H:%M')

        instance = model_class(**data)
        db.session.add(instance)
        db.session.commit()
        return instance

class ListService:
    @staticmethod
    def execute(model_class):
        return model_class.query.all()

class FindByIdService:
    @staticmethod
    def execute(model_class, id):
        return model_class.query.get_or_404(id)

class UpdateService:
    @staticmethod
    def execute(model_class, id, data):
        instance = model_class.query.get_or_404(id)
        for key, value in data.items():
            if value == '':
                value = None
            if key in ['data', 'data_inscricao', 'data_envio'] and isinstance(value, str) and value:
                value = datetime.strptime(value, '%Y-%m-%d').date()
            elif key == 'horario' and isinstance(value, str) and value:
                if len(value) == 5:
                    value += ":00"
                value = datetime.strptime(value, '%H:%M:%S').time()
            elif key == 'data_hora' and isinstance(value, str) and value:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M')

            setattr(instance, key, value)
        db.session.commit()
        return instance

class DeleteService:
    @staticmethod
    def execute(model_class, id):
        instance = model_class.query.get_or_404(id)
        db.session.delete(instance)
        db.session.commit()
        return True
