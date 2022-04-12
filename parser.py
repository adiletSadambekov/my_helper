from config import names_items

from bs4 import BeautifulSoup
import requests


class PageParse:
    url = 'http://namaz-time.ru/moscow'

    def get_page(self):
        return requests.get(self.url)
    
    def get_page_parse(self):
        return BeautifulSoup(self.get_page().text, 'html.parser')
    
    def get_items_times(self):
        time = []
        items = self.get_page_parse().findAll('div', class_='today__item__time')
        for n,t in enumerate(items):
            time.append(names_items[n] + t.text)
        return time