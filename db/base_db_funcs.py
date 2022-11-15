from data import config
from .base import CreateAndCloseSession
from .models import *
from aiogram.types.user import User as UserTG

from .exceptions import *

from utills.notifyes import notify_owner

import logging

from typing import List

path_log = 'App.db.base_db_funcs'

logging.getLogger(path_log)


class UsersBaseFunctions(CreateAndCloseSession):
    logger = logging.getLogger(path_log + '.BaseFunctions')

    def is_exists_by_tg(self, id_in_tg) -> User:
        logger = logging.getLogger(path_log + '.BaseFunctions.is_exists')
        try:
            user = self.s.query(User).where(User.id_in_tg == id_in_tg).scalar()
            if user:
                return user
            else:
                return False
        except Exception as e:
            logger.exception(e)


    def get_all_users_by_city(self, id_city: int) -> List[User]:
        logger = logging.getLogger(path_log + '.BaseFunctions.get_all_users')
        try:
            users = self.s.query(User).where(User.is_active == True).where(
                User.id_city == id_city).all()
            if users:
                return users
            else:
                return False
        except Exception as e:
            notify_owner(config.OWNER_ID)
            logger.exception(e)
    

    def add_user(self, user_date: UserTG):
        logger = logging.getLogger(path_log + '.BaseFunctions.add_user')
        try:
            user_exists = self.is_exists_by_tg(user_date.id)
            if user_exists:
                raise ErrorAddUser('User is added yet')
            else:
                user = User(
                    user_date.id,
                    user_date.username,
                    user_date.full_name)
                self.s.add(user)
                self.s.commit()
                return user
        except Exception as e:
            logger.exception(e)

    

    def get_user(self, user_id: int) -> User:
        logger = logging.getLogger(path_log + '.BaseFunctions.get_user')
        try:
            user = self.s.query(User).where(User.id_in_tg == user_id).scalar()
            if user:
                return user
            else:
                return False
        except Exception as e:
            logger.exception(e)


    def unsubscribe(self, user_id) -> bool:
        logger = logging.getLogger(path_log + '.BaseFunctions.unsubscribe')
        try:  
            user = self.get_user(user_id)
            if user:
                user.is_active = False
                self.s.commit()
                return user
            else:
                return False
        except Exception as e:
            logger.exception(e)


    def repoll_city(self, user_id: int, id_city: int) -> UserTG:
        logger = logging.getLogger(path_log + '.BaseFunctions.repolls_city')
        try:
            user = self.get_user(user_id)
            if user:
                user.id_city = id_city
                self.s.commit()
            else:
                return False
        except Exception as e:
            logger.exception(e)


    def subscribe(self, user_data: UserTG, id_city=None) -> User:
        logger = logging.getLogger(path_log + '.BaseFunctions.subscribe')
        try:
            user = self.get_user(user_data.id)
            if user:
                if user.id_city and user.is_active == False:
                    user.is_active = True
                    self.s.commit()
                    return user
                else:
                    user.id_city = id_city
                    user.is_active = True
                    self.s.commit()
                    return user
            else:
                False
        except Exception as e:
            logger.exception(e)
    

    def unsubscrieb(self, user_id: int) -> User:
        logger = logging.getLogger(path_log + '.BaseFunctions.unsubscribe')
        try:
            user = self.get_user(user_id=user_id)
            user.is_active = False
            self.s.commit()
            return user
        except Exception as e:
            logger.exception(e)



class CityesBaseFunctions(CreateAndCloseSession):
    logging.getLogger(path_log + '.CityesBaseFunctions')

    def get_all_cityes(self) -> City:
        logger = logging.getLogger(path_log + '.CityesBaseFunctions.get_all_cityes')
        try:
            cityes = self.s.query(City).all()
            if cityes:
                return cityes
            else:
                return False
        except Exception as e:
            logger.exception(e)
    

    def get_city(self, city_id: int):
        logger = logging.getLogger(path_log + '.CityesBaseFunctions.get_city')
        try:
            city =self.s.query(City).where(City.id == city_id).scalar()
            if city:
                return city
            else: 
                return False
        except Exception as e:
            logger.exception(e)
