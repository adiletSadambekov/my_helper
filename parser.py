
from config import names_items

from bs4 import BeautifulSoup
import requests


class PageParse:
    url = 'https://www.vremyanamaza.ru/Центральный/время-намаза-Москва/19400-tat17'

    def get_page(self):
        return requests.get(self.url)
    
    def get_page_parse(self):
        return BeautifulSoup(self.get_page().content, 'html.parser')
    
    def get_items_times(self):
        times = []
        items = self.get_page_parse().findAll('div', class_='right floated content prayerTime')
        for n, d in enumerate(items):
            times.append(names_items[n]+d.text)
        times = [i.replace('\t', '') for i in times]
        return times