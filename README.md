# newsletter-webappnews

## Newsletter service
- RTLINFO main page scraping
- Generation of a Wordcloud to summarize news titles 
- Wordcloud Picture sent by mail (from noreply.webappnews@gmail.com)

## Crontab automation
crontab job scheduled every weekday (monday to friday) at 11.50 am
```
50 11 * * 1-5 /Users/emelinevanderbeken/.pyenv/versions/newsletter_webappnews/bin/python /Users/emelinevanderbeken/PycharmProjects/newsletter_news/main.py
```