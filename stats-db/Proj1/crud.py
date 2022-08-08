from sqlalchemy.orm import Session
import models, schemas


def get_users(db: Session):
    return db.query(models.Usuarios).all()

def get_user_by_cpf(db: Session, id: int):
    return db.query(models.Usuarios).filter(models.Usuarios.cpf == id).first()

def get_data_by_username(db: Session, id: int):
    return db.query(models.Dados).filter(models.Dados.user == id).first()

def get_all_data(db: Session):
    return db.query(models.Dados).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_new_user = models.Usuarios(name=user.name, cpf=user.cpf)
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    return db_new_user


def create_data(db: Session, user:str, ox:int, bpm:int):

    # print ("*"*100, (data.__dict__))
    # print("\n", data.bpm , "\n", data.ox, "\n")
    db_new_data = models.Dados(user=user, ox=ox, bpm=bpm)

    

    # db_userId = db.query(models.Usuarios).filter(models.Usuarios.cpf == str(data.userId)).first()
    # if db_userId is not None:
    db.add(db_new_data)
    db.commit()
    db.refresh(db_new_data)
    return db_new_data

    # return None

# def create_nota(db: Session, nota: schemas.NotaCreate, disciplina: str):
#     db_nota = models.Notas(disciplina=disciplina, titulo=nota.titulo, descricao=nota.descricao)

#     db_disciplina = db.query(models.Notas).filter( (models.Notas.disciplina == disciplina), (models.Notas.titulo == nota.titulo)).first()

#     if db_disciplina is None:
#         db.add(db_nota)
#         db.commit()
#         db.refresh(db_nota)
#         return db_nota
#     return None


# def delete_disciplina(db: Session, nome: str):
#     return db.query(models.Disciplinas).filter(models.Disciplinas.name == nome).delete()
    
# def delete_nota(db: Session, titulo: str, disciplina: str):
#     return db.query(models.Notas).filter((models.Notas.titulo == titulo), (models.Notas.disciplina == disciplina)).delete()
    

# def update_disciplina(db: Session, infos: schemas.DisciplinaUpdate, nome: str):
#     db_disciplina = db.query(models.Disciplinas).filter(models.Disciplinas.name == str(nome)).first()
#     if infos.name is not None:
#         db_disciplina.name = infos.name
#     if infos.prof_name is not None:
#         db_disciplina.prof_name = infos.prof_name
#     db.commit()
#     db.refresh(db_disciplina)
#     return db_disciplina