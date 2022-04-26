from array import array
from email.policy import default
from config import engin

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'subs'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, unique=True)
    username = Column(String)
    userlogin = Column(String)
    is_active = Column(Boolean, default=True)
