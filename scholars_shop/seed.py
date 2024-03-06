import sqlite3

conn = sqlite3.connect('scholars.db')
c = conn.cursor()

# Seed categories data
categories = [
    ('Food',),
    ('Fashion',),
    ('Books',),
    ('Gadgets',),
    ('Electronics',)
]

products = [
    ( "iPhone promax 13", "sdfkhskfjg" , "iphone13.jpg", 5)
]

#c.executemany("INSERT INTO categories (name) VALUES (?)", categories)


c.executemany("INSERT INTO products (name, description, image, cat_id) VALUES (?,?,?,?)", products)

conn.commit()
conn.close()