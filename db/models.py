from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users(Base):
    __tablename__ = 'subs'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, unique=True)
    username = Column(String)
    userlogin = Column(String)
    is_active = Column(Boolean, default=True)
    permession = Column(String(20))

class Times(Base):
    __tablename__ = 'namases_times'
    id = Column(Integer, primary_key=True)
    items = Column(String, nullable=False)
