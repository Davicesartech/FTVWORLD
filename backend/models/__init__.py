# ============================================================================
# __INIT__.PY (pasta models)
# ============================================================================
# Este arquivo faz o Python tratar a pasta "models" como um "pacote"
# (um conjunto de arquivos .py relacionados que podem ser importados
# em conjunto).
#
# Além disso, ele REEXPORTA todas as Models e o "db", para que o resto
# do projeto possa importar de forma simples:
#
#     from models import Usuario, Campeonato, db
#
# Em vez de precisar saber o nome exato do arquivo onde cada Model
# está guardada (ex: "from models.usuario import Usuario").
# ============================================================================

from models.db_instance import db
from models.usuario import Usuario
from models.campeonato import Campeonato
from models.quadra import Quadra
from models.inscricao import Inscricao
from models.dupla import Dupla
from models.partida import Partida
from models.notificacao import Notificacao
