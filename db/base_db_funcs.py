"""# importing utills
from utills.utills import write_excep
import json

#importing library orm system sqlalchemy
from sqlalchemy.orm import sessionmaker

#importing models
from models import Users, Times

#importin utills
from datetime import datetime

# configutation data
from users.conf.config import engin

from parser.parser import PageParse"""

from data import config
from .base import CreateAndCloseSession
from .models import *

from parser.parser import ItemsParse

import logging
import json

logging.getLogger('App.db.base_db_funcs')


class ForItems(CreateAndCloseSession):
    logger = logging.getLogger('App.db.base_db_funcs.ForItems')
    def add_actual_items(
        self,
        items: ItemsParse.get_items_times) -> bool:

        logger = logging.getLogger(
            'App.db.base_db_funcs.ForItems.add_actual')

        try:
            times = Times(items='\n'.join(items))
            self.s.add(times)
            self.s.commit()
            return True
        except Exception as e:
            logger.exception(e)
            return False
    
    def update_items(self, items: ItemsParse.get_items_times) -> bool:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForItems.update_items')

        try:
            old_items = self.s.query(Times).where(Times.id == 1).scalar()
            if old_items:
                old_items.items = '\n\n'.join(items)
                self.s.commit()
                return True
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False
    
    def get_items(self) -> str:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForItems.get_items')

        try:
            items = self.s.query(Times).where(Times.id == 1).scalar()
            if items:
                return items
            else:
                None
        except Exception as e:
            logger.exception(e)
            return False

        


class ForUsers(CreateAndCloseSession):
    logger = logging.getLogger('App.db.base_db_funcs.ForUsers')

    def is_exists(self, id_user: int) -> bool:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForUsers.is_exists')

        try:
            exists = self.s.query(Users).where(
                Users.id_user == id_user).count()
            if exists:
                return exists
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False


    def get_all_users(self) -> list:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForUsers.get_all_users')

        try:
            users = self.s.query(Users).all()
            if users:
                return users
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False
    
    def get_all_active(self) -> list:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForUsers.get_all_active')
        try:
            users = self.s.query(Users).where(
                Users.is_active == True).all()
            if users:
                return users
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False  


    def get_user(self, id_user: int) -> Users:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForUsers.get_user')

        try:
            exists = self.is_exists(id_user)
            if exists:
                user = self.s.query(Users).where(
                    Users.id_user == id_user).scalar()
                return user
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False
    
    
    def add_user(self, users_data) -> bool:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForUsers.add_user')

        try:
            user = self.s.query(Users).where(Users.id_user == users_data.id).scalar()
            if user:
                if user.is_active == False:
                    user.is_active = True
                    self.s.commit()
                    return 3 # for indetify about resubscribe
                else:
                    return 2
            else:
                user = Users(
                    id_user=users_data.id,
                    userlogin=users_data.username,
                    username=users_data.full_name,
                    permession='user')
                self.s.add(user)
                self.s.commit()
                return True
        except Exception as e:
            logger.exception(e)
            return False


    def unsubscribe(self, id_user: int) -> bool:
        logger = logging.getLogger(
            'App.db.base_db_funcs.ForUsers.add_user')
            
        try:
            user = self.get_user(id_user)
            if user:
                user.is_active = False
                self.s.commit()
            else:
                None
        except Exception as e:
            logger.exception(e)
            return False
    


class ForAdmin(CreateAndCloseSession):
    logging.getLogger('App.db.base_db_funcs')

    def get_all_users(self) -> list:
        logger = logging.getLogger('App.db.base_db_funcs.get_users_in_json')
        try:
            users = self.s.query(Users).all()
            if users:
                return users
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False
    


'''class DBForUser:

    now = datetime.now()

    def __init__(self):
        Session = sessionmaker(engin)
        self.s = Session()

    def subscribe(self, id_user, username, userlogin):
        try:
            new_user = Users(id_user=id_user, username=username, userlogin=userlogin)
            Session = sessionmaker(engin)
            with Session() as s:
                exists_ = s.query(Users).where(Users.id_user == id_user).scalar()
                if exists_:
                    if exists_.is_active == False:
                        exists_.is_active = True
                        s.commit()
                        return 'Вы обнавили подписку'
                    else:
                        return 'Вы и так подписаны'
                s.add(new_user)
                s.commit()
                return  f"Дорогой(ая) {username}, вы успешно подписались на рассылку"
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'add_user')
            return 'Не удалось подписаться'
    
    def rm_user(self, id_user):
        try:
            Session = sessionmaker(bind=engin)
            with Session() as s:
                exists_ = s.query(Users).filter(Users.id_user == id_user).one()
                if not exists_:
                    return 'Вы и так не подписаны'
                else:
                    s.delete(exists_)
                    s.commit()
                    return f"Дорогой(ая) {exists_.username}, вы успушно удалили свои данные из базы данных"
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'rm_user')
            return 'Не удалось удалить ваши данные, обратитесь к админу'


    def get_all_active(self): #geting all users data
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                data = s.query(Users).where(Users.is_active == 1)
                return data
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'get_all')
            return False
    
    def get_user(self, id_user): # function for geting one user
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                user = s.query(Users).where(Users.id_user == id_user).scalar()
                if user:
                    return True, user
                else:
                    return True, 'Такого пользователя не существует'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'get_user')
            return False
    
    def update_data(self, obj): # function for update users data
                                # parametr obj is class with three atribets
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                exists_ = s.query(Users).where(Users.id_user == obj.id_user).scalar()
                if exists_:
                    exists_.username = obj.username
                    exists_.userlogin = obj.userlogin
                    s.commit()
                    return True, 'Данные успешно обновлены'
                else:
                    return 'Такого пользователя не существует'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'update_data')
            return False
        

    def unsubscribe(self, id_user):
        try:
            Session = sessionmaker(engin)
            with Session() as s:
                exists = s.query(Users).where(Users.id_user == id_user).scalar()
                if exists:
                    if exists.is_active == False:
                        return 'Вы и так отписаны от рассылку'
                    elif exists.is_active == True:
                        exists.is_active = False
                        s.commit()
                        return 'Вы успешно отписались от рассылки'
                else:
                    return 'Вы и так не подписаны на рассылку. Чтобы подписаться на рассылку\
                        необходимо ввести комманду /start'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'unsubscribe')
            return False
    

    def get_users_in_json(self):
        try:
            users = self.s.query(Users).all()
            data = {'users':{'user':{
                'id': n.id,
                'id_user': n.id_user,
                'username': n.username,
                'userlogin': n.userlogin,
                'is_active': n.is_active }for n in users}}

            return json.dumps(data)
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'DBForUser.get_users_in_json')
            return 'Не удалось получить данные'

    
    def __del__(self):
        self.s.close()


class DBForItems:

    def __init__(self):
        self.Session = sessionmaker(engin)
        self.s = self.Session()

    def add_items(self):
        try:
            time_items = PageParse().get_items_times()
            if time_items:
                model_times = Times(items='\n\n'.join(time_items))
                self.s.add(model_times)
                self.s.commit()
                return True
            else:
                return 'Warning'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'DBForItems.add_items')
            return False
    
    def update_items(self):
        try:
            time_items = PageParse().get_items_times()
            if time_items:
                items_collection = '\n\n'.join(time_items)
                old_items = self.s.query(Times).where(Times.id == 1).scalar()
                old_items.items = items_collection
                self.s.commit()
                write_excep('Times is updated in db', 'message.txt', 'update')
                return True
            else:
                return 'Warning'
        except Exception as e:
            write_excep(e, 'logfile_db.txt', 'DBForItem.update_items')
            return False
    
    def get_items(self):
        try:
            items = self.s.query(Times).where(Times.id == 1).scalar()
            return items
        except Exception as e:
            write_excep(e, 'ligfile_db.txt', 'DBForItems.get_items')
            return False
    
    def __del__(self):
        self.s.close()'''