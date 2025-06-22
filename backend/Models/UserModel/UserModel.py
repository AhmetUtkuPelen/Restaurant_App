from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'



class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)