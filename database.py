# database.py

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tarefas.db"  # URL para o banco de dados SQLite

# Criando o motor de conexão
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criando a sessão para as operações com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
metadata = MetaData()
