from data import config
from .exceptions import ReceivedIncorrectResponse

from bs4 import BeautifulSoup
import requests
import logging

from dataclasses import dataclass, replace
from datetime import time
import re

logging.getLogger('App.parser.parser')

@dataclass(slots=True, frozen=True)
class NamazesTimes:
    fajr: time
    sunrise: time
    dhuhr: time
    asr: time
    magrib: time
    isha: time



class ParsingNTimes:
    def get_namazes_times(self) -> NamazesTimes:
        logger = logging.getLogger('App.parser.parser.get_namazes_times')
        try:
            headers = {'user-agent': config.USER_AGENT}
            page = requests.get(config.URL_FOR_PARSER, headers=headers)
            if page.status_code == 200:
                html_doc = BeautifulSoup(page.content, 'html.parser')
                div_items = html_doc.find('div',
                class_='columns small-up-2 large-up-6 medium-up-3 time-block')
                items = div_items.findAll('span', class_='text-center rb')
                return NamazesTimes(
                    items[0].text,
                    items[1].text,
                    items[2].text,
                    items[3].text,
                    items[4].text,
                    items[5].text)
            else:
                raise ReceivedIncorrectResponse(page.status_code)
        except Exception as e:
            logger.exception(e)
            return False #think about return value
    
    def formatter_for_image(self) -> list:
        items = self.get_namazes_times()
        if items:
            names_items = [i.replace(' ', '') for i in config.ITEMS_NAMES]
            items_list = [
                names_items[0] + '\n\n' + items.fajr + '\n',
                names_items[1] + '\n\n' + items.sunrise + '\n',
                names_items[2] + '\n\n' + items.dhuhr + '\n',
                names_items[3] + '\n\n' + items.asr + '\n',
                names_items[4] + '\n\n' + items.magrib + '\n',
                names_items[5] + '\n\n' + items.isha + '\n',
            ]
            return items_list


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
