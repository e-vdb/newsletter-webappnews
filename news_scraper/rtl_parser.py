
import logging
from bs4 import BeautifulSoup
import requests
import pandas as pd


logging.basicConfig(level=logging.INFO)


class RtlParser:
    def __init__(self):
        self.articles = None

    def collect_content(self, url):
        source = requests.get(url).content
        soup = BeautifulSoup(source, 'html.parser')
        self.articles = soup.find_all('r-viewmode')

    @staticmethod
    def parse_article(article):
        title = article.h3.text
        category = article.find('r-article--meta').text
        image = article.find('img')['data-srcset'].split(',')[0].split(' ')[0]
        return title, category, image

    def extract_articles(self):
        rtl_main_content = []
        for article in self.articles:
            try:
                title, category, image = self.parse_article(article)
                row = {'title': title, 'category': category, 'image': image}
                rtl_main_content.append(row)
            except Exception:
                pass
        return pd.DataFrame(
            rtl_main_content,
            columns=['title', 'category', 'image']
        )

