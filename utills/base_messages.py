from data import config
import json
import logging

logging.getLogger('App.utills.base_messages')

def get_items_message(id_city: int) -> str:
    logger = logging.getLogger('App.utills.base_messages.get_items_message')
    try:
        with open(config.PATH_TIMES_FILE, 'r') as f:
            items = json.load(f)
        items_city = items[str(id_city)]
        if items_city:
            message = [items_city[item][0] + ' - ' + \
                items_city[item][1] for item in items_city]
            return str(message).replace("'", '').replace(
                '[', ''
            ).replace(']', '').replace(',', '\n\n')
        else:
            return 'Данный город еще не добавлен в список этого проекта'
    except Exception as e:
        logger.exception(e)

    
    