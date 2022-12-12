from .models import *
from .base import CreateAndCloseSession

from data import config

import logging

logging.getLogger(config.APP_LOG_FILE + '.db.db_owner_funcs')

class OwnerDBFunctions(CreateAndCloseSession):
    
    def add_city(self, name: str, full_name: str) -> City:
        logger = logging.getLogger(
            config.APP_LOG_FILE + '.db.db_owner_funcs.OwnerDBFunctions.add_city')
        try:
            city = City(name, full_name)
            self.s.add(city)
            self.s.commit()
            get_city = self.s.query(City).where(
                City.name == name).where(
                    City.full_name == full_name).scalar()
            if get_city:
                return get_city
            else:
                return None
        except Exception as e:
            logger.exception(e)
            return False
