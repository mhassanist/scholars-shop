from flask import Flask, render_template, redirect, url_for, request
import sqlite3


app = Flask(__name__)

def create_database():
    conn = sqlite3.connect('scholars.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                 )''')

    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                 )''')
    
    # Seed categories data
    categories = [
        ('food',),
        ('fashion',),
        ('books',),
        ('gadgets',),
        ('electronics',)
    ]

    c.executemany("INSERT INTO categories (name) VALUES (?)", categories)

    c.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                image BLOB NOT NULL,
                category_id INT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
                )''')
    
    # Seed products data
    sample_products = [
        ('Product 1', 'Description 1', 'image1.jpg', 1),
        ('Product 2', 'Description 2', 'image2.jpg', 2),
        ('Product 3', 'Description 3', 'image3.jpg', 3),
        ('Product 4', 'Description 4', 'image4.jpg', 4),
        ('Product 5', 'Description 5', 'image5.jpg', 5),
        ('Product 6', 'Description 6', 'image6.jpg', 1)
    ]

    c.executemany("INSERT INTO products (name, description, image, category_id) VALUES (?, ?, ?, ?)", sample_products)

    conn.commit()
    conn.close()


@app.route('/')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('scholars.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return "Username already exists. Please choose a different one."
        
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login_page'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('scholars.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            return "Login successful"
        else:
            return "Invalid username or password"
        
    return render_template ('login.html') 

@app.route('/product/<category>')
def show_product(category):
    food_menu_links = ["Breakfast", "Lunch", "Dinner", "Desserts", "Drinks"]
    books_menu_links =["Science", "Art", "Engineering", "Finance"]
    fashion_menu_links =["Clothes", "Bags", "Shoes", "Jewelries"]
    electronics_menu_links = ["Television", "Air-conditioners", "Refrigerator", "Fans"]
    gadgets_menu_links = ["Phones", "Laptops", "Gaming", "Accesories"]

    food_image ="main_food.png"
    fashion_image="main_fashion.png"
    books_image ="main_books.png"
    gadgets_image ="main_gadgets.png"
    electronics_image ="main_electronics.png"

    menu_links = []
    banner_img = ""
    if category == "food":
        menu_links = food_menu_links
        banner_img = food_image
    elif category == "fashion":
        menu_links = fashion_menu_links
        banner_img = fashion_image
    elif category == "books":
        menu_links = books_menu_links
        banner_img = books_image
    elif category == "gadgets":
        menu_links = gadgets_menu_links
        banner_img = gadgets_image
    elif category == "electronics":
        menu_links = electronics_menu_links
        banner_img = electronics_image

    conn = sqlite3.connect('scholars.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products p JOIN categories c ON p.category_id = c.id WHERE c.name =?", (category,))
    items = c.fetchall()
    conn.close

    return render_template("products.html", products = items, category = category, menu_links=menu_links, banner_img = banner_img)


@app.route('/products/<cat_id>')
def show_products(cat_id):
    # cat_id = request.args.get('cat_id')

    if cat_id is not None:
        cat_id = int(cat_id)

        # Fetch products based on the specified category
        conn = sqlite3.connect('scholars.db')
        c = conn.cursor()

        c.execute("SELECT * FROM products WHERE cat_id=?", (cat_id,))
        products_data = c.fetchall()

        conn.close()

        return render_template('products.html', products=products_data, category_id=cat_id)
    else:
        conn = sqlite3.connect('scholars.db')
        c = conn.cursor()

        c.execute("SELECT * FROM products")
        products_data = c.fetchall()

        conn.close()

        return render_template('products.html', products=products_data, category_id=None)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)


   
    