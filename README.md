# newsletter-webappnews

![daily_cronjob](https://github.com/e-vdb/newsletter-webappnews/actions/workflows/run_app.yml/badge.svg)
![pylint](https://github.com/e-vdb/newsletter-webappnews/actions/workflows/pylint.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Newsletter service
- RTLINFO main page scraping
- Generation of a Wordcloud to summarize news titles 
- Wordcloud Picture sent by mail (from noreply.webappnews@gmail.com)

## Crontab automation
crontab job scheduled every weekday (monday to friday) at 11.50 am
```
50 11 * * 1-5 /Users/emelinevanderbeken/.pyenv/versions/newsletter_webappnews/bin/python /Users/emelinevanderbeken/PycharmProjects/newsletter_news/main.py
```

## Documentation

### Sending email with Python
https://geekflare.com/send-gmail-in-python/

### Crontab automation
https://www.jcchouinard.com/python-automation-with-cron-on-mac/