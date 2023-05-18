import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        self.page = requests.get(self.url)
        self.content = self.page.content
