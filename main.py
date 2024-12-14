from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def get_articles_and_authors(selected_author=None):
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()
    if selected_author:
        cursor.execute(
            'SELECT title, link, content FROM articles WHERE author = ?', (selected_author,)
        )
    else:
        cursor.execute('SELECT title, link, content FROM articles')
    articles = cursor.fetchall()
    cursor.execute('SELECT DISTINCT author FROM articles')
    authors = [row[0] for row in cursor.fetchall()]

    conn.close()
    return articles, authors


@app.route('/')
def index():
    selected_author = request.args.get('author')
    articles, authors = get_articles_and_authors(selected_author)
    return render_template('index.html',
                           articles=articles,
                           authors=authors,
                           selected_author=selected_author)


if __name__ == '__main__':
    app.run(debug=True)
