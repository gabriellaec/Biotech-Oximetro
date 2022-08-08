from sqlalchemy.orm import Session
import models, schemas

def get_users(db: Session):
    return db.query(models.Usuarios).all()

def get_user_by_cpf(db: Session, id: int):
    return db.query(models.Usuarios).filter(models.Usuarios.cpf == id).first()

def get_data_by_username(db: Session, id: int):
    return db.query(models.Dados).filter(models.Dados.user == id).all()

def get_all_data(db: Session):
    return db.query(models.Dados).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_new_user = models.Usuarios(name=user.name, cpf=user.cpf)
    db.add(db_new_user)
    db.commit()
    db.refresh(db_new_user)
    return db_new_user


def create_data(db: Session, user:str, ox:int, bpm:int):
    db_new_data = models.Dados(user=user, ox=ox, bpm=bpm)
    db.add(db_new_data)
    db.commit()
    db.refresh(db_new_data)
    return db_new_data