import os
import sqlite3
from makelinkstxt import get_link_from_line, get_text_from_line

if not 'db' in os.listdir():
    os.mkdir('db')

db = sqlite3.connect('db/links')
cursor = db.cursor()

cursor.execute('''CREATE TABLE links(id INTEGER PRIMARY KEY, link TEXT, description TEXT)''')

with open('./lines.csv', 'r') as f:
    lines = f.readlines()

links = []
for line in lines:
    item = (get_link_from_line(line), get_text_from_line(line))
    links.append(item)

for link in links:
    cursor.execute('''insert into links(link, description) values(?, ?)''', link)


def add_tags_to_db():
    tags = ['r', 'algorithms', 'probability', 'statistics', 'ml', 'datasets', 'neuralnets', 'deeplearning', 'nlp', 'social', 'latex', 'ide', 'javascript', 'python', 'linearalgebra', 'pandas', 'plots', 'numpy', 'datascience']
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE tags(id INTEGER PRIMARY KEY, name TEXT unique)''')

    for t in tags:
         cursor.execute('''insert into tags(name) values(?)''', (t, ))
