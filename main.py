#O comando uvicorn main:app se refere a:
#main: o arquivo main.py (o "módulo" Python).
#app: o objeto criado no arquivo main.py com a linha app = FastAPI().
#--reload: faz o servidor reiniciar após mudanças de código. Use apenas para desenvolvimento.
#
#http://127.0.0.1:8000/docs  -> testando a api

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models import Tarefa
from database import engine, SessionLocal, Base
from pydantic import BaseModel

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Modelo de dados para API (Pydantic)
class TarefaCreate(BaseModel):
    titulo: str
    descricao: str = None
    concluida: bool = False

class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: str
    concluida: bool

    class Config:
        from_attributes = True     ##-> alteração significativa


# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tarefas/", response_model=TarefaResponse)
async def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = Tarefa(**tarefa.dict())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@app.get("/tarefas/", response_model=List[TarefaResponse])
async def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(Tarefa).all()

@app.get("/tarefas/{tarefa_id}", response_model=TarefaResponse)
async def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=TarefaResponse)
async def atualizar_tarefa(tarefa_id: int, tarefa: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    for key, value in tarefa.dict().items():
        setattr(db_tarefa, key, value)

    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}")
async def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(db_tarefa)
    db.commit()
    return {"message": "Tarefa deletada com sucesso"}