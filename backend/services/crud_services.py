# ============================================================================
# CRUD_SERVICES.PY
# ============================================================================
# CAMADA SERVICE: representa os CASOS DE USO da aplicação.
#
# Cada classe abaixo representa UM ÚNICO caso de uso (ex: "criar um
# usuário", "listar todos os campeonatos"). Isso é diferente de ter um
# único Service genérico fazendo tudo — aqui, cada operação de cada
# entidade tem sua própria classe, facilitando adicionar regras de
# negócio específicas no futuro (ex: validações, envio de e-mail,
# notificações) sem misturar a lógica de diferentes casos de uso.
#
# IMPORTANTE: o Service NUNCA acessa o banco de dados diretamente.
# Ele apenas CHAMA os métodos que já existem na Model (que por sua vez
# usam o CRUDMixin). Isso mantém a separação de responsabilidades:
#   Controller -> recebe a requisição HTTP
#   Service    -> executa o caso de uso (a "regra do negócio")
#   Model      -> conversa com o banco de dados
# ============================================================================
from models import Usuario, Campeonato, Quadra, Inscricao, Dupla, Partida, Notificacao


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Usuario
# ---------------------------------------------------------------------------

class CreateUsuarioService:
    """Caso de uso: criar um novo registro de Usuario."""
    @staticmethod
    def execute(dados):
        return Usuario.criar(dados)


class ListUsuarioService:
    """Caso de uso: listar todos os registros de Usuario."""
    @staticmethod
    def execute():
        return Usuario.listar()


class FindUsuarioByIdService:
    """Caso de uso: buscar um registro de Usuario por ID."""
    @staticmethod
    def execute(id):
        return Usuario.buscar_por_id(id)


class UpdateUsuarioService:
    """Caso de uso: atualizar um registro existente de Usuario."""
    @staticmethod
    def execute(id, dados):
        return Usuario.atualizar(id, dados)


class DeleteUsuarioService:
    """Caso de uso: remover um registro de Usuario."""
    @staticmethod
    def execute(id):
        return Usuario.deletar(id)


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Campeonato
# ---------------------------------------------------------------------------

class CreateCampeonatoService:
    """Caso de uso: criar um novo registro de Campeonato."""
    @staticmethod
    def execute(dados):
        return Campeonato.criar(dados)


class ListCampeonatoService:
    """Caso de uso: listar todos os registros de Campeonato."""
    @staticmethod
    def execute():
        return Campeonato.listar()


class FindCampeonatoByIdService:
    """Caso de uso: buscar um registro de Campeonato por ID."""
    @staticmethod
    def execute(id):
        return Campeonato.buscar_por_id(id)


class UpdateCampeonatoService:
    """Caso de uso: atualizar um registro existente de Campeonato."""
    @staticmethod
    def execute(id, dados):
        return Campeonato.atualizar(id, dados)


class DeleteCampeonatoService:
    """Caso de uso: remover um registro de Campeonato."""
    @staticmethod
    def execute(id):
        return Campeonato.deletar(id)


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Quadra
# ---------------------------------------------------------------------------

class CreateQuadraService:
    """Caso de uso: criar um novo registro de Quadra."""
    @staticmethod
    def execute(dados):
        return Quadra.criar(dados)


class ListQuadraService:
    """Caso de uso: listar todos os registros de Quadra."""
    @staticmethod
    def execute():
        return Quadra.listar()


class FindQuadraByIdService:
    """Caso de uso: buscar um registro de Quadra por ID."""
    @staticmethod
    def execute(id):
        return Quadra.buscar_por_id(id)


class UpdateQuadraService:
    """Caso de uso: atualizar um registro existente de Quadra."""
    @staticmethod
    def execute(id, dados):
        return Quadra.atualizar(id, dados)


class DeleteQuadraService:
    """Caso de uso: remover um registro de Quadra."""
    @staticmethod
    def execute(id):
        return Quadra.deletar(id)


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Inscricao
# ---------------------------------------------------------------------------

class CreateInscricaoService:
    """Caso de uso: criar um novo registro de Inscricao."""
    @staticmethod
    def execute(dados):
        return Inscricao.criar(dados)


class ListInscricaoService:
    """Caso de uso: listar todos os registros de Inscricao."""
    @staticmethod
    def execute():
        return Inscricao.listar()


class FindInscricaoByIdService:
    """Caso de uso: buscar um registro de Inscricao por ID."""
    @staticmethod
    def execute(id):
        return Inscricao.buscar_por_id(id)


class UpdateInscricaoService:
    """Caso de uso: atualizar um registro existente de Inscricao."""
    @staticmethod
    def execute(id, dados):
        return Inscricao.atualizar(id, dados)


class DeleteInscricaoService:
    """Caso de uso: remover um registro de Inscricao."""
    @staticmethod
    def execute(id):
        return Inscricao.deletar(id)


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Dupla
# ---------------------------------------------------------------------------

class CreateDuplaService:
    """Caso de uso: criar um novo registro de Dupla."""
    @staticmethod
    def execute(dados):
        return Dupla.criar(dados)


class ListDuplaService:
    """Caso de uso: listar todos os registros de Dupla."""
    @staticmethod
    def execute():
        return Dupla.listar()


class FindDuplaByIdService:
    """Caso de uso: buscar um registro de Dupla por ID."""
    @staticmethod
    def execute(id):
        return Dupla.buscar_por_id(id)


class UpdateDuplaService:
    """Caso de uso: atualizar um registro existente de Dupla."""
    @staticmethod
    def execute(id, dados):
        return Dupla.atualizar(id, dados)


class DeleteDuplaService:
    """Caso de uso: remover um registro de Dupla."""
    @staticmethod
    def execute(id):
        return Dupla.deletar(id)


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Partida
# ---------------------------------------------------------------------------

class CreatePartidaService:
    """Caso de uso: criar um novo registro de Partida."""
    @staticmethod
    def execute(dados):
        return Partida.criar(dados)


class ListPartidaService:
    """Caso de uso: listar todos os registros de Partida."""
    @staticmethod
    def execute():
        return Partida.listar()


class FindPartidaByIdService:
    """Caso de uso: buscar um registro de Partida por ID."""
    @staticmethod
    def execute(id):
        return Partida.buscar_por_id(id)


class UpdatePartidaService:
    """Caso de uso: atualizar um registro existente de Partida."""
    @staticmethod
    def execute(id, dados):
        return Partida.atualizar(id, dados)


class DeletePartidaService:
    """Caso de uso: remover um registro de Partida."""
    @staticmethod
    def execute(id):
        return Partida.deletar(id)


# ---------------------------------------------------------------------------
# Casos de uso da entidade: Notificacao
# ---------------------------------------------------------------------------

class CreateNotificacaoService:
    """Caso de uso: criar um novo registro de Notificacao."""
    @staticmethod
    def execute(dados):
        return Notificacao.criar(dados)


class ListNotificacaoService:
    """Caso de uso: listar todos os registros de Notificacao."""
    @staticmethod
    def execute():
        return Notificacao.listar()


class FindNotificacaoByIdService:
    """Caso de uso: buscar um registro de Notificacao por ID."""
    @staticmethod
    def execute(id):
        return Notificacao.buscar_por_id(id)


class UpdateNotificacaoService:
    """Caso de uso: atualizar um registro existente de Notificacao."""
    @staticmethod
    def execute(id, dados):
        return Notificacao.atualizar(id, dados)


class DeleteNotificacaoService:
    """Caso de uso: remover um registro de Notificacao."""
    @staticmethod
    def execute(id):
        return Notificacao.deletar(id)
