from data import config
from .exceptions import ReceivedIncorrectResponse

from bs4 import BeautifulSoup
import requests
import logging

from dataclasses import dataclass
from datetime import time

logging.getLogger('App.parser.parser')


class NamazesTimes:
    def __init__(self, fajr, sunrise, dhuhr, asr, magrib, isha) -> None:
        self.fajr = fajr
        self.sunrise = sunrise
        self.dhuhr = dhuhr
        self.asr = asr
        self.magrib = magrib
        self.isha = isha



class ParsingNTimes:
    def get_namazes_times(self, name_city: str) -> NamazesTimes:
        logger = logging.getLogger('App.parser.parser.get_namazes_times')
        try:
            headers = {'user-agent': config.USER_AGENT}
            page = requests.get(config.URL_FOR_PARSER + name_city, headers=headers)
            if page.status_code == 200:
                html_doc = BeautifulSoup(page.content, 'html.parser')
                div_items = html_doc.find('div',
                class_='columns small-up-2 large-up-6 medium-up-3 time-block')
                items = div_items.findAll('span', class_='text-center rb')
                return NamazesTimes(
                    [config.ITEMS_NAMES[0], items[0].text],
                    [config.ITEMS_NAMES[1], items[1].text],
                    [config.ITEMS_NAMES[2], items[2].text],
                    [config.ITEMS_NAMES[3], items[3].text],
                    [config.ITEMS_NAMES[4], items[4].text],
                    [config.ITEMS_NAMES[5], items[5].text])
            else:
                raise ReceivedIncorrectResponse(page.status_code)
        except Exception as e:
            logger.exception(e)
            return False #think about return value
    
    def get_to_dict(self, name_city: str) -> list:
        items = self.get_namazes_times(name_city)
        if items:
            items_dict = {
                'fajr': items.fajr,
                'sunrise': items.sunrise,
                'dhuhr': items.dhuhr,
                'asr': items.asr,
                'magrib': items.magrib,
                'isha': items.isha,
            }
            return items_dict
