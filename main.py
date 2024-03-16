from flask import Flask, request, render_template, session, redirect, url_for
import mysql.connector
from flask import flash

app = Flask(__name__)
app.secret_key = 'mombasa'  # Set a strong and random secret key

# Landing page route
@app.route('/')
def index():
    return render_template('index.html')


# Connect to MySQL database
def connect_to_database():
    connection= mysql.connector.connect(
        host='192.168.1.89',
        port='3306',
        user='dartboss',
        password='Blackcat111@',
        database='monate'
    )
    return connection



# Sign-up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        email = request.form['email']
        password = request.form['password']
        
        try:
            connection = connect_to_database()
            cursor = connection.cursor()
            
            # SQL query and parameters
            sql = "INSERT INTO monate_users(customer_name, email, password) VALUES (%s, %s, %s)"
            val = (customer_name, email, password)
            
            cursor.execute(sql, val)
            connection.commit()
            
            cursor.close()
            connection.close()  # Close the connection after use
            flash('You have successfully signed up!')  # Add a flash message (optional)
            return redirect(url_for('login'))  # Redirect to the login page after signup (optional)
        except mysql.connector.Error as err:
            return f"An error occurred: {err}"
    else:
        return render_template('signup.html')  # Render the signup form

from flask import render_template

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # If the user is logged in, render the index.html template
        return render_template('dashboard.html')
    else:
        # If the user is not logged in, redirect them to the login page
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Received POST request to /login. Email: {email}, Password: {password}")

        # Check if email and password match a user in the database
        connection= connect_to_database()
        cursor = connection.cursor()
        sql = "SELECT * FROM monate_users WHERE email = %s AND password = %s"
        val= (email, password)
        cursor.execute(sql, val)    
        user = cursor.fetchone()
        connection.close()

        if user:
            session['email'] = email
            return redirect(url_for('dashboard'))  # Redirect to the index route if login is successful
        else:
            return 'Invalid email or password. Please try again.'

    return render_template('login.html')  # Render a login form HTML template

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))  # Redirect to the index route after logout


#class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    connection = connect_to_database()
    cursor = connection.cursor()
    sql = "SELECT id, product, image_path, description, price FROM gallery"
    cursor.execute(sql)
    # Fetch data from the gallery table
    data = cursor.fetchall()
    return render_template('gallery.html', gallery=data)

if __name__ == '__main__':
    app.run(debug=True)
