import sqlite3
import cursor
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('articles.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL
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
        author = "-"
        for elements in data_link.findAll('div', class_='container-item__author'):
            if elements.a.text is not None:
                cleaned_text = " ".join(elements.a.text.split())
                author = cleaned_text
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
                        INSERT INTO articles (title, link, author, content) VALUES (?, ?, ?, ?)
                        ''', (title, link, author, content))

        conn.commit()


cursor.execute('SELECT * FROM articles')
users = cursor.fetchall()

for user in users:
    print(user)

conn.close()

