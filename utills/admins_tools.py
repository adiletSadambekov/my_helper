from data import config
from db.base_db_funcs import ForAdmin

import json
import logging

from sqlalchemy import create_engine

logging.getLogger('App.utills.admins_tools')

def save_users_json() -> None:
    logger = logging.getLogger('App.utills.admins_tools.save_users_json')
    users_in_json = {}
    try:
        engine = create_engine(config.PATH_DB)
        users = ForAdmin(engine).get_all_users()
        if users:
            for n, i in enumerate(users):
                users_in_json['user' + str(n)] = {
                'id_user' : i.id_user,
                'username' : i.username,
                'userlogin' : i.userlogin,
                'is_active' : i.is_active,
                'permession' : i.permession
                }
        with open('data/' + config.LIST_USERS, 'w') as f:
            f.write(json.dumps(users_in_json))
    except Exception as e:
        logger.exception(e)
        return False

