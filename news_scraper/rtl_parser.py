from bs4 import BeautifulSoup
import requests
import pandas as pd


class RtlParser:
    def __init__(self):
        self.results = None

    def collect_content(self, url):
        source = requests.get(url).content
        soup = BeautifulSoup(source, 'html.parser')
        self.results = soup.find('div', id='w-content')

    def find_main_article(self, class_, site):
        articles = self.results.find_all("div", class_=class_)
        df_articles = pd.DataFrame(columns=['title', 'category', 'summary', 'image', 'link'])
        for article in articles:
            title = article.h1.text
            category = article.find('span', class_="category").text
            summary = article.p.text
            url = article.find('a')['href'].lstrip('//')
            url = url.lstrip('www.rtl.be/')
            link = 'https://www.rtl.be/' + url
            if site == 'actu':
                try:
                    image = article.find('img')['data-wdosrc']
                except:
                    image = None
            else:
                try:
                    image = article.find('img')['src']
                except KeyError:
                    image = article.find('img')['data-original']

            row = {'title': title, 'category': category, 'summary': summary, 'image': image, 'link': link}
            df_articles = df_articles.append(row, ignore_index=True)
        return df_articles
