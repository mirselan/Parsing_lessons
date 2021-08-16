from lxml import html
import requests
import re
from pymongo import MongoClient


def news_to_db(x):  # Функция для записи вакансий в базу данных
    client = MongoClient('127.0.0.1', 27017)
    db = client['ai_1054_news']

    lenta_news = db.lenta_news
    lenta_news.insert_one(x)


url = 'https://lenta.ru/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                              AppleWebKit/537.36 (KHTML, like Gecko)\
                              Chrome/90.0.4430.93 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

news = dom.xpath("//div[@class='item'] | //div[@class='first-item']")

for news_1 in news:
    news_data = {}
    source_name = url
    name = news_1.xpath("./a/text() | ./h2/a/text()")
    link = news_1.xpath("./a/@href")
    date = news_1.xpath(".//time/@datetime")

# Обработка полученных списков в строки и удаление мусорных символов
    name_0 = str(name)
    news_link_0 = url + str(link)
    date_0 = str(date)
    news_link = re.sub('[\[|\]|\']', '', news_link_0)
    news_name_1 = re.sub('[\[|\]|\']', '', name_0)
    news_name = news_name_1.replace('\\xa0', ' ')
    news_date = re.sub('[\[|\]|\']', '', date_0)

# Сборка данных в словарь
    news_data['1_sourse_url'] = source_name
    news_data['2_news_name'] = news_name
    news_data['3_news_link'] = news_link
    news_data['4_news_date'] = news_date

# Запись полученных данных в базу данных
    news_to_db(news_data)





