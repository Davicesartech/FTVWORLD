# ============================================================================
# DB_INSTANCE.PY
# ============================================================================
# Este arquivo tem uma única responsabilidade: criar a instância do
# SQLAlchemy (o ORM - Object Relational Mapper - usado para transformar
# classes Python em tabelas do banco de dados, sem precisar escrever SQL
# manualmente para o CRUD básico).
#
# POR QUE ISSO FICA EM UM ARQUIVO SEPARADO?
# Se colocássemos "db = SQLAlchemy()" dentro de um dos arquivos de Model
# (ex: usuario.py), todos os outros arquivos de Model precisariam importar
# o "db" DAQUELE arquivo específico, criando uma dependência confusa entre
# eles. Com "db" isolado aqui, qualquer arquivo do projeto pode importar
# de forma simples e sem risco de "import circular" (quando o arquivo A
# depende do B, que depende do A, travando o programa).
# ============================================================================

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
