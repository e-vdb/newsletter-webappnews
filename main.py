from newsletter.newsletter import Newsletter


def main():
    news = Newsletter()
    news.generate_wordcloud()
    print('Wordcloud picture generated')
    news.send_newsletter()
    print("Email sent to subscribers")


if __name__ == '__main__':
    main()
