from typing import Optional
from fastapi import FastAPI, status, Form, Request, HTTPException
from fastapi.param_functions import Path
from pydantic import BaseModel, Field
from typing import List, Dict
from starlette.responses import RedirectResponse
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        "name": "Usuários",
        "description": "Pessoas cadastradas",
    },
    {
        "name": "Dados",
        "description": "Oximetria e frequência cardíaca",
    },
]

description = """
    Microsserviço de controle de dados para para gerenciar oximetria e frequência cardíaca 🚀
"""


app = FastAPI(
    title="Oxímetro",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# #---------------------------------------------------#
# #    	             Usuarios    	            #
# #---------------------------------------------------#
# #####################################################
# # • O usuário pode criar uma disciplina
# #####################################################
@app.post("/oximetro/newuser/",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar usuário",
response_description="Adicionando Usuário",
response_model=schemas.User,
tags=["Usuários"]
)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_cpf(db, user.cpf)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado!")
    return crud.create_user(db=db, user=user)


# #####################################################
# #R • Listar os pacientes
# #####################################################
@app.get("/oximetro/users",
status_code=status.HTTP_200_OK,
summary="Listar pacientes",
response_description="Listando os pacientes",
tags=["Usuários"]
)
def get_all_users( db: Session = Depends(get_db)):
    """
     Lista todos os pacientes
    """

    db_users = crud.get_users(db)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Nenhum usuário cadastrado")

    return db_users


#---------------------------------------------------#
#    	                 Notas    	                #
#---------------------------------------------------#
#######################################################
#C • O usuário pode adicionar uma nota a uma disciplina
#######################################################
@app.post("/oximetro/{user}/data",  
status_code=status.HTTP_201_CREATED,
summary="Adicionar Dados",
response_description="Adicionando dado",
response_model=schemas.Data,
tags=["Dados"]
)

def create_entry(
    userId: int, ox:int, bpm:int, db: Session = Depends(get_db)
):
    """
    Cria uma entrada com os dados de freq cardiaca e oximetria
    """

    db_user = crud.get_user_by_cpf(db, id=userId)
    if db_user is None:
        
        raise HTTPException(status_code=404, detail="Usuario não encontrado!")
    print ("-------" *10, userId)

    query = crud.create_data(db=db, user = db_user.id, ox=ox, bpm=bpm)
    if query is None:
        raise HTTPException(status_code=404, detail="Já existe uma nota com esse nome nesta disciplina!")
   
    return query

# #####################################################
# #R • Listar os dados de um paciente
# #####################################################
@app.get("/oximetro/{user_id}/data",
status_code=status.HTTP_200_OK,
summary="Listar dados de um paciente",
response_description="Listando os dados",
response_model=schemas.Data,
tags=["Dados"]
)
def get_entry_by_userId(user_id: int, db: Session = Depends(get_db)):
    """
     Lê todos os dados de um paciente
    - **user_id**: CPF do paciente
    """

    db_user = crud.get_user_by_cpf(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario não encontrado!")

    db_data = crud.get_data_by_username(db, id=db_user.id)
    if db_data is None:
        raise HTTPException(status_code=404, detail="Não existem dados para este paciente!")

    return db_data


# #####################################################
# #R • Listar os dados
# #####################################################
@app.get("/oximetro/all_data",
status_code=status.HTTP_200_OK,
summary="Listar dados",
response_description="Listando os dados",
tags=["Dados"]
)
def get_all_data( db: Session = Depends(get_db)):
    """
     Lista todos os dados
    """

    db_users = crud.get_all_data(db)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Nenhum dado cadastrado")

    return db_users