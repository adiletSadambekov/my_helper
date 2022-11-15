from data import config
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_name = Column(String)
    users = relationship('User', back_populates='city')

    def __init__(self, name: str, full_name: str) -> None:
        self.name = name
        self.full_name = full_name


class AccesLevel(Base):
    __tablename__ = 'acces_level'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    level = Column(Integer)
    description = Column(String(240))
    users = relationship('User', back_populates='acces_level')

    def __init__(self, name: str, level: int, description: str):
        self.name = name
        self.level = level
        self.description = description


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    id_in_tg = Column(Integer, unique=True)
    username = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=False)
    id_city = Column(Integer, ForeignKey('city.id'))
    id_acces_level = Column(Integer, ForeignKey('acces_level.id'), default=config.FIRST_USERS_ACCES)
    acces_level = relationship('AccesLevel', back_populates='users')
    city = relationship('City', back_populates='users')

    def __init__(self, id_in_tg: int, username: str, full_name: str) -> None:
        self.id_in_tg = id_in_tg
        self.username = username
        self.full_name = full_name


