from data import config

from db.models import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


enginge = create_engine(config.PATH_DB)

def create_models() -> bool:
    try:
        Base.metadata.create_all(enginge)
        return True
    except:
        return False

def add_acces_levels() -> bool:
    try:
        user_level = AccesLevel('user', 10, 'This is users level an its first level')
        admin_level = AccesLevel('admin', 20, 'This is admin level')
        owner_level = AccesLevel('owner', 30, 'This is higher acces level')
        Session = sessionmaker(enginge)
        s = Session()
        s.add_all([user_level, admin_level, owner_level])
        s.commit()
        return True
    except Exception as e:
        print(e)
    finally:
        s.close_all()