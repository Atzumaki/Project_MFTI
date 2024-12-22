from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import sqlite3
import requests
import datetime
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def create_database():
        conn = sqlite3.connect('../articles.db')
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
        conn.close()

    def selenium_get(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service()
        driver = webdriver.Firefox(options=options, service=service)
        try:
            driver.get(self.url)

            wait = WebDriverWait(driver, 10)

            try:
                cookie_banner = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cookie-consent__button"))
                )
                cookie_banner.click()
            except Exception:
                pass

            for _ in range(3):
                button = wait.until(
                    EC.element_to_be_clickable((By.ID, "btnShowMore"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", button)
                button.click()
            html = driver.page_source
        finally:
            driver.quit()

        return html

    def response(self):
        conn = sqlite3.connect('../articles.db')
        cursor = conn.cursor()
        response = requests.get(self.url)
        response.raise_for_status()
        html = self.selenium_get()

        data = BeautifulSoup(html, 'html.parser')

        for article in data.findAll('h2', class_='item-title text-short'):
            if article.a:
                title = article.a.text.strip()
                link = 'https://utv.ru/' + article.a['href']

                response_link = requests.get(link)
                response_link.raise_for_status()
                data_link = BeautifulSoup(response_link.text, 'html.parser')
                date_div = data_link.find('div', class_="container-item__metrics item-metrics")
                if date_div and date_div.span:
                    raw_date = date_div.span.text.strip()
                    date = self.check_date(raw_date)
                else:
                    date = "-"
                author_div = data_link.find('div', class_='container-item__author')
                if author_div and author_div.a:
                    author = author_div.a.text.strip()
                else:
                    author = "-"
                paragraphs = data_link.findAll('p')
                content = []
                for p in paragraphs:
                    text = p.text.strip()
                    if text:
                        content.append(text)
                content = " ".join(content)
                cursor.execute('''SELECT title, date FROM articles''')
                issue = cursor.fetchall()
                if issue:
                    flag = 1
                    for title_base, date_base in issue:
                        if title_base == title and date_base == date:
                            flag = 0
                            break
                    if flag:
                        cursor.execute('''
                        INSERT INTO articles (title, link, author, content, date) VALUES (?, ?, ?, ?, ?)
                        ''', (title, link, author, content, date))
                else:
                    cursor.execute('''
                                    INSERT INTO articles (title, link, author, content, date) VALUES (?, ?, ?, ?, ?)
                                    ''', (title, link, author, content, date))

        conn.commit()
        conn.close()

    def parse_date(self, date_str):
        months = {
            "января": "01",
            "февраля": "02",
            "марта": "03",
            "апреля": "04",
            "мая": "05",
            "июня": "06",
            "июля": "07",
            "августа": "08",
            "сентября": "09",
            "октября": "10",
            "ноября": "11",
            "декабря": "12",
        }
        parts = date_str.split()
        day = parts[0]
        month = months[parts[1]]
        time = parts[3]
        current_year = datetime.datetime.now().year
        date_formatted = f"{day}.{month}.{current_year}.{time}"
        return date_formatted

    def check_date(self, date):
        if "час" in date:
            h = int(date.split()[0])
            time_minus_one_hour = datetime.datetime.now() - datetime.timedelta(hours=h)
            return time_minus_one_hour.strftime('%d.%m.%Y.%H:%M')
        elif "минут" in date:
            m = int(date.split()[0])
            time_minus_one_hour = datetime.datetime.now() - datetime.timedelta(minutes=m)
            return time_minus_one_hour.strftime('%d.%m.%Y.%H:%M')
        elif "сегодня" in date:
            t = date.split()[2]
            return datetime.datetime.now().strftime('%d.%m.%Y') + f'.{t}'
        elif "вчера" in date:
            t = date.split()[2]
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            return yesterday.strftime('%d.%m.%Y') + f'.{t}'
        else:
            a = self.parse_date(date)
            return a

# Вывод
# cursor.execute('SELECT * FROM articles')
# users = cursor.fetchall()
#
# for user in users:
#     print(user)
#
# conn.close()
