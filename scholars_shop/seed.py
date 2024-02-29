import sqlite3

conn = sqlite3.connect('scholars.db')
c = conn.cursor()

# Seed categories data
categories = [
    ('Food',),
    ('Fashion',),
    ('Computing',),
    ('Phones',),
    ('Electronics',)
]

c.executemany("INSERT INTO categories (name) VALUES (?)", categories)

conn.commit()
conn.close()