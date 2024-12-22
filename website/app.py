from flask import Flask, render_template, request
import sqlite3
from parser_database import Parser

url = "https://utv.ru/"

app = Flask(__name__)

parser = Parser(url)
parser.create_database()
parser.response()


def get_articles_and_authors(selected_author=None, search_issue=None):
    conn = sqlite3.connect('../articles.db')
    cursor = conn.cursor()
    issue = 'SELECT title, link, content, date FROM articles'
    params = []

    if selected_author and search_issue:
        issue += ' WHERE author = ? AND title LIKE ? ORDER BY date DESC'
        params.extend([selected_author, f"%{search_issue}%"])
    elif selected_author:
        issue += ' WHERE author = ? ORDER BY date DESC'
        params.append(selected_author)
    elif search_issue:
        issue += ' WHERE title LIKE ? ORDER BY date DESC'
        params.append(f"%{search_issue}%")
    else:
        issue += ' ORDER BY date DESC'

    cursor.execute(issue, params)
    articles = cursor.fetchall()

    cursor.execute('SELECT DISTINCT author FROM articles')
    authors = [row[0] for row in cursor.fetchall()]

    conn.close()
    return articles, authors


@app.route('/')
def index():
    selected_author = request.args.get('author')
    search_issue = request.args.get('search', '').strip()
    articles, authors = get_articles_and_authors(selected_author, search_issue)

    return render_template('index.html',
                           articles=articles,
                           authors=authors,
                           selected_author=selected_author,
                           search_query=search_issue,
                           )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5252)
