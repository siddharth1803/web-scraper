import csv
import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json

conn = sqlite3.connect('theverge.db')
curr = conn.cursor()

curr.execute('''
    CREATE TABLE IF NOT EXISTS articles
    (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, headline TEXT, author TEXT, date TEXT)
''')

url = "https://www.theverge.com/"

code = requests.get(url).text
soup = BeautifulSoup(code, 'html.parser')
data = soup.find('script', attrs={'id': '__NEXT_DATA__'})

json_data = json.loads(data.text)
articles = json_data.get("props").get("pageProps").get("mostPopularData")

data = []
i = 0

for article in articles:
    headline = article.get("title")
    url = article.get("url")
    author = article.get("author").get("fullName")
    date = article.get("publishDate")
    curr.execute('INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)',
                 (url, headline, author, date))
    data.append((i, url, headline, author, date))
    i = i + 1

filename = 'ddmmyyy_verge.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'URL', 'headline', 'author', 'date'])
    writer.writerows(data)

conn.commit()
conn.close()
