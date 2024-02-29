from flask import Flask, render_template, redirect, url_for, request
import sqlite3


app = Flask(__name__)

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

        return redirect(url_for('login'))

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

@app.route('/products/<cat_id>')
def show_products():
    cat_id = request.args.get('cat_id')

    if cat_id is not None:
        cat_id = int(cat_id)

        # Fetch products based on the specified category
        conn = sqlite3.connect('products.db')
        c = conn.cursor()

        c.execute("SELECT * FROM products WHERE cat_id=?", (cat_id,))
        products_data = c.fetchall()

        conn.close()

        return render_template('products.html', products=products_data, category_id=cat_id)
    else:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()

        c.execute("SELECT * FROM products")
        products_data = c.fetchall()

        conn.close()

        return render_template('products.html', products=products_data, category_id=None)

if __name__ == '__main__':
    app.run(debug=True)
