from data import config

from bs4 import BeautifulSoup
import requests
import logging

logging.getLogger('App.parser.parser')

class ItemsParse:
    logger = logging.getLogger('App.parser.parser.ItemsParse')
    url = 'https://www.vremyanamaza.ru/Центральный/время-намаза-Москва/19400-tat17'

    page = None

    def __init__(self) -> None:
        logger = logging.getLogger('App.parser.parser.ItemsParse.__init__')
        try:
            self.page = requests.get(self.url)
        except Exception as e:
            logger.exception(e)

    
    def get_page_parse(self):
        return BeautifulSoup(self.page.content, 'html.parser')
    
    def get_items_times(self) -> list:
        logger = logging.getLogger(
            'App.parser.parser.ItemsParse.get_items_times')
        try:
            times = []
            items = self.get_page_parse().findAll(
                'div',
                class_='right floated content prayerTime')
            items_name = config.ITEMS_NAME.split(',')
            for n, d in enumerate(items):
                times.append(items_name[n] + '\n' +d.text)
            times = [i.replace('\t', '') for i in times]
            return times
        except Exception as e:
            logger.exception(e)
            return False
