import logging

from wordcloud import WordCloud
from cleantext import clean
from datetime import datetime
from pathlib import Path
from os.path import dirname, join
from dotenv import load_dotenv

from news_scraper.rtl_parser import RtlParser
from mail.mail_attachment import Mail
from mail.utils import get_env_var
from mail.constants import (
    EMAILS
)

now = datetime.now()
load_dotenv()


logging.basicConfig(level=logging.INFO)


class Newsletter:
    def __init__(self):
        self.articles = None

    @staticmethod
    def load_mails():
        return get_env_var(EMAILS).split(",")

    def generate_wordcloud(self):
        categories = ['ACTU', 'SPORT']
        for category in categories:
            self.scrape(category)
            self.save_wordcloud(category)

    def scrape(self, category):
        if category == 'ACTU':
            self.scrape_rtl()
        else:
            self.scrape_rtl_sport()

    def scrape_rtl(self):
        rtl_parser = RtlParser()
        rtl_parser.collect_content(url='https://www.rtl.be')
        self.articles = rtl_parser.extract_articles()

    def scrape_rtl_sport(self):
        rtl_parser = RtlParser()
        rtl_parser.collect_content(url='https://www.rtl.be/sport')
        self.articles = rtl_parser.extract_articles()

    def save_wordcloud(self, category):
        words = self.clean_text(" ".join(self.articles['title'].values))
        self.setup_wordcloud(words, category)

    @staticmethod
    def setup_wordcloud(words, category):
        stopwords = ['un', 'une', 'pour', 'et', 'le', 'la', 'de', 'sur', 'ca', 'ce', 'celui', 'a', 'en', 'les', 'des',
                     'lui', 'ont', 'video', 'qui', 'tres', 'deja', 'il', 'elle', 'lui', 'du', 'ne', 'pas', 'se',
                     'son', 'sa', 'dans', 'photo', 'apres', 'au', 'par', 'est', 'avec', 'voici', "d'un", "d'une",
                     "photos", "videos", 'ans', 'ete', "encore", "sous", "sur", "je", "tu", "pour", "n'", "deux",
                     "apres", 'avant', 'mais', "qu'",  "quoi", "que", "leur", "va", "cette", "plus"]
        wordcloud = WordCloud(colormap='YlOrRd', stopwords=stopwords)
        wordcloud.generate(words)
        filename = 'wordcloud_' + category + '_' + now.strftime("%d_%m_%Y") + '.png'
        pictures_dir = join(Path(dirname(__file__)).parent, 'wordcloud_fig')
        filepath = join(pictures_dir, filename)
        wordcloud.to_file(filepath)

    @staticmethod
    def clean_text(text):
        cleaned_text = clean(text,
                                        fix_unicode=True,  # fix various unicode errors
                                        to_ascii=True,  # transliterate to closest ASCII representation
                                        lower=True,  # lowercase text
                                        no_line_breaks=True,
                                        # fully strip line breaks as opposed to only normalizing them
                                        no_urls=True,  # replace all URLs with a special token
                                        no_emails=True,  # replace all email addresses with a special token
                                        no_phone_numbers=True,  # replace all phone numbers with a special token
                                        no_numbers=False,  # replace all numbers with a special token
                                        no_digits=False,  # replace all digits with a special token
                                        no_currency_symbols=True,  # replace all currency symbols with a special token
                                        no_punct=False,  # remove punctuations
                                        replace_with_punct=".",  # instead of removing punctuations you may replace them
                                        replace_with_url="<URL>",
                                        replace_with_email="<EMAIL>",
                                        replace_with_phone_number="<PHONE>",
                                        replace_with_number="<NUMBER>",
                                        replace_with_digit="0",
                                        replace_with_currency_symbol="<CUR>",
                                        lang="en"  # set to 'de' for German special handling
                                        )
        return cleaned_text

    def send_newsletter(self):
        mail = Mail()
        mails = self.load_mails()
        mail.send(mails)
