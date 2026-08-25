# ============================================================================
# CRUD_MIXIN.PY
# ============================================================================
# O QUE É UM "MIXIN"?
# Um Mixin é uma classe que não representa uma entidade sozinha, mas que
# "empresta" métodos prontos para outras classes, através de herança
# múltipla. Em vez de escrever os mesmos 5 métodos de CRUD (criar, listar,
# buscar, atualizar, deletar) dentro de cada uma das 7 Models do projeto,
# escrevemos uma única vez aqui, e cada Model apenas "herda" esse
# comportamento.
#
# ONDE ISSO É USADO?
# Toda classe de Model (Usuario, Campeonato, Quadra, etc.) é declarada
# assim:
#     class Usuario(db.Model, CRUDMixin):
#
# Isso significa: "Usuario é uma tabela do banco (db.Model) E também usa
# os métodos do CRUDMixin". A partir disso, é possível chamar diretamente:
#     Usuario.criar(dados)
#     Usuario.listar()
#     Usuario.buscar_por_id(5)
#     Usuario.atualizar(5, dados)
#     Usuario.deletar(5)
#
# POR QUE ISSO É IMPORTANTE NA ARQUITETURA DO PROJETO?
# A camada Model é responsável pela representação das entidades E pelo
# CRUD básico. Colocando os métodos aqui (e cada Model herdando deles),
# garantimos que o CRUD "mora" na Model — e não na camada de Service,
# que deveria apenas ORQUESTRAR o caso de uso, sem falar diretamente
# com o banco de dados.
# ============================================================================

from datetime import datetime
from models.db_instance import db

# Nomes de campos que representam data/hora, e o formato em que o
# frontend (input type="date"/"time"/"datetime-local") os envia.
# Usado para converter o TEXTO recebido do formulário em objetos
# date/time/datetime de verdade, ANTES de gravar no banco — evitando
# que um campo de data fique salvo como string pura (o que quebra a
# formatação depois, na hora de listar os registros).
_CAMPOS_DATA = {
    'data': ('%Y-%m-%d', 'date'),
    'data_inscricao': ('%Y-%m-%d', 'date'),
    'data_envio': ('%Y-%m-%d', 'date'),
    'horario': ('%H:%M', 'time'),
    'data_hora': ('%Y-%m-%dT%H:%M', 'datetime'),
}


class CRUDMixin:
    """
    Mixin com os métodos básicos de CRUD (Create, Read, Update, Delete).
    Reaproveitado por todas as 7 Models do projeto (Usuario, Campeonato,
    Quadra, Inscricao, Dupla, Partida, Notificacao).
    """

    @staticmethod
    def _converter_datas(dados):
        """
        Percorre o dicionário recebido do frontend e converte os campos
        de data/hora (que chegam como TEXTO em JSON) para objetos Python
        de verdade (date/time/datetime). Campos vazios ("") viram None,
        em vez de serem salvos como texto inválido no banco.
        """
        convertido = dict(dados)
        for campo, (formato, tipo) in _CAMPOS_DATA.items():
            if campo not in convertido:
                continue
            valor = convertido[campo]
            if not isinstance(valor, str):
                continue  # já é um objeto de data, ou é None
            if valor.strip() == '':
                convertido[campo] = None
                continue
            try:
                if tipo == 'date':
                    convertido[campo] = datetime.strptime(valor, formato).date()
                elif tipo == 'time':
                    texto = valor if len(valor) > 5 else valor  # "HH:MM"
                    convertido[campo] = datetime.strptime(texto[:5], formato).time()
                elif tipo == 'datetime':
                    convertido[campo] = datetime.strptime(valor[:16], formato)
            except ValueError:
                # Não foi possível interpretar o texto como data/hora
                # válida — melhor guardar None do que travar a aplicação.
                convertido[campo] = None
        return convertido

    @classmethod
    def criar(cls, dados):
        """
        Cria um novo registro no banco.
        'cls' é a própria classe que chamou o método (ex: Usuario).
        'dados' é um dicionário com os campos, ex: {"nome": "João", "email": "..."}.
        """
        dados = cls._converter_datas(dados)
        novo = cls(**dados)          # cria uma instância da Model com os dados recebidos
        db.session.add(novo)          # marca o objeto para ser inserido
        db.session.commit()           # efetivamente grava no banco
        return novo

    @classmethod
    def listar(cls):
        """Retorna todos os registros da tabela correspondente à Model."""
        return cls.query.all()

    @classmethod
    def buscar_por_id(cls, id):
        """Busca um único registro pelo ID. Retorna None se não existir."""
        return cls.query.get(id)

    @classmethod
    def atualizar(cls, id, dados):
        """
        Atualiza um registro existente.
        Só altera os campos que vierem no dicionário 'dados' — os demais
        continuam com o valor que já tinham.
        """
        registro = cls.query.get(id)
        if not registro:
            return None  # registro não encontrado

        dados = cls._converter_datas(dados)
        for chave, valor in dados.items():
            if hasattr(registro, chave):   # só atualiza campos que existem na Model
                setattr(registro, chave, valor)

        db.session.commit()
        return registro

    @classmethod
    def deletar(cls, id):
        """Remove um registro do banco. Retorna True/False indicando sucesso."""
        registro = cls.query.get(id)
        if not registro:
            return False

        db.session.delete(registro)
        db.session.commit()
        return True
