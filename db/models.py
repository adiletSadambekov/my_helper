from data import config
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class TimeZone(Base):
    __tablename__ = 'time_zone'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cityes = relationship('City', back_populates='time_zone')

    def __init__(self, name):
        self.name = name


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    id_timezone = Column(Integer, ForeignKey('time_zone.id'))
    users = relationship('User', back_populates='city')
    time_zone = relationship('TimeZone', back_populates='cityes')

    def __init__(self, name: str, full_name: str) -> None:
        self.name = name
        self.full_name = full_name


class AccesLevel(Base):
    __tablename__ = 'acces_level'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    level = Column(Integer, nullable=False)
    description = Column(String(240))
    users = relationship('User', back_populates='acces_level')

    def __init__(self, name: str, level: int, description: str):
        self.name = name
        self.level = level
        self.description = description


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    id_in_tg = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=False)
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


