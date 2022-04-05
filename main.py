from newsletter.newsletter import Newsletter
import os
from pathlib import Path
from os.path import dirname, join


def main():
    news = Newsletter()
    news.generate_wordcloud()
    print('Wordcloud picture generated')
    news.send_newsletter()
    print("Email sent to subscribers")


if __name__ == '__main__':
    try:
        os.makedirs(join(Path(dirname(__file__)), 'wordcloud_fig'))
    except OSError as e:
        print('folder already exists')
    main()
