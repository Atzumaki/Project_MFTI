import sqlite3
import cursor
import requests
import datetime
from bs4 import BeautifulSoup

current_date = ".".join((datetime.datetime.now().strftime('%d-%m-%Y')).split('-'))
print(current_date)


def check_date(date):
    if "час назад" in date:
        return current_date
    elif "вчера" in date:
        try:
            return str(int(current_date.split('.')[0]) - 1) + current_date.split('.')[1] + current_date.split('.')[2]
        except Exception as e:
            return ""
    else:
        return_date = ''
        for item in date:
            if item == 'в':
                break
            return_date += item
        return return_date[:-2]


conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    date TEXT NOT NULL
)
''')



conn.commit()


url = "https://utv.ru/ufa/t/novosti/"

response = requests.get(url).text

data = BeautifulSoup(response, 'html.parser')
for article in data.findAll('h2', class_='item-title text-short'):
    if article.a is not None:
        title = article.a.text
        link = 'https://utv.ru/' + article.a['href']
        response_link = requests.get(link).text
        data_link = BeautifulSoup(response_link, 'html.parser')
        date = "-"
        for day in data_link.findAll('div', class_="container-item__metrics item-metrics"):
            if day.span.text is not None:
                date = " ".join(day.span.text.split())
                date = check_date(date)
        author = "-"
        for elements in data_link.findAll('div', class_='container-item__author'):
            if elements.a.text is not None:
                author = " ".join(elements.a.text.split())
        bag = []
        for elements in data_link.findAll('p'):
            if elements.text is not None:
                for i in elements.text.split('\xa0'):
                    if i != '':
                        bag.append(i)
                if len(bag) % 2 == 0 and len(bag) != 0:
                    break
        content = " ".join(bag)

        cursor.execute('''
                        INSERT INTO articles (title, link, author, content, date) VALUES (?, ?, ?, ?, ?)
                        ''', (title, link, author, content, date))

        conn.commit()

# Вывод
# cursor.execute('SELECT * FROM articles')
# users = cursor.fetchall()
#
# for user in users:
#     print(user)
#
# conn.close()

