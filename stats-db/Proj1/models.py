from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import VARCHAR
from database import Base
from sqlalchemy.sql import func


class Usuarios(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name =  Column(VARCHAR(200),  index=True)
    cpf = Column(Integer, unique=True, index=True)


class Dados(Base):

    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    ox =  Column(Integer)
    bpm =  Column(Integer)
    datetime = Column(DateTime(timezone=True), server_default=func.now())
    