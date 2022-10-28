from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'milestone2'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def Home():
   return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def Contact():
   return render_template('index.html')


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def userLogin():
   # Output message if something goes wrong...
   msg = ''
   # Check if "email" and "password" POST requests exist (user submitted form)
   if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       # Create variables for easy access
       username = request.form['username']
       password = request.form['password']
       # Check if account exists using MySQL
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM User WHERE username = %s AND password = %s', (username, password,))
       # Fetch one record and return result
       account = cursor.fetchone()
       # If account exists in accounts table in out database
       if account:
           # Create session data, we can access this data in other routes
           session['loggedin'] = True
           session['ID'] = account['ID']
           session['username'] = account['username']
           # Redirect to home page
           return redirect(url_for('userHome'))
       else:
           # Account doesnt exist or username/password incorrect
           msg = 'Incorrect username/password!'
   # Show the login form with message (if any)
   return render_template('login.html', msg=msg)


# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
   # Output message if something goes wrong...
   msg = ''
   # Check if "email" and "password" POST requests exist (user submitted form)
   if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       # Create variables for easy access
       username = request.form['username']
       password = request.form['password']
       # Check if account exists using MySQL
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM Admin WHERE username = %s AND password = %s', (username, password,))
       # Fetch one record and return result
       account = cursor.fetchone()
       # If account exists in accounts table in out database
       if account:
           # Create session data, we can access this data in other routes
           session['loggedin'] = True
           session['ID'] = account['ID']
           session['username'] = account['username']
           # Redirect to home page
           return redirect(url_for('adminHome'))
       else:
           # Account doesnt exist or username/password incorrect
           msg = 'Incorrect username/password!'
   # Show the login form with message (if any)
   return render_template('adminLogin.html', msg=msg)


@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('ID', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('userLogin'))


# http://localhost:5000/Falsk/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register2', methods=['GET', 'POST'])
def userRegister():
   # Output message if something goes wrong...
   msg = ''
   # Check if "username", "password" and "email" POST requests exist (user submitted form)
   if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
       # Create variables for easy access
       email = request.form['email']
       password = request.form['password']
       username = request.form['username']

       # Check if account exists using MySQL
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM User WHERE username = %s AND email = %s', (username, email,))
       account = cursor.fetchone()
       # If account exists show error and valIDation checks
       if account:
           msg = 'Account already exists!'
       elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
           msg = 'InvalID email address!'
       elif not username or not password or not email:
           msg = 'Please fill out the form!'
       else:
           # Account doesnt exists and the form data is valID, now insert new account into accounts table
           cursor.execute('INSERT INTO User (username, email, password) VALUES (%s,%s, %s)', (username, email, password,))
           mysql.connection.commit()
           msg = 'You have successfully registered!'

   elif request.method == 'POST':
       # Form is empty... (no POST data)
       msg = 'Please fill out the form!'
   # Show registration form with message (if any)
   return render_template('register.html', msg=msg)


# http://localhost:5000/pythinlogin/userHome - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def userHome():
   # Check if user is loggedin
   if 'loggedin' in session:
       # User is loggedin show them the home page
       return render_template('userHome.html', username=session['username'])
   # User is not loggedin redirect to login page
   return redirect(url_for('userLogin'))


# http://localhost:5000/pythinlogin/adminHome - this will be the home page, only accessible for loggedin admins
@app.route('/adminHome/home')
def adminHome():
   # Check if user is loggedin
   if 'loggedin' in session:
       # User is loggedin show them the home page
       return render_template('adminHome.html', username=session['username'])
   else:
       # User is not loggedin redirect to login page
       return redirect(url_for('userLogin'))


@app.route('/addItem', methods=['GET', 'POST'])
def addItem():
   # Output message if something goes wrong...
   msg = ''
   # Check if "brand", "name", "releaseDate", "discNumber", "abbreviation", and "cost" POST requests exist (user submitted form)
   if request.method == 'POST' and 'brand' in request.form and 'name' in request.form and 'release_date' in request.form and 'disc_number' in request.form and 'abbreviation' in request.form and 'cost' in request.form:
       # Create variables for easy access
       brand = request.form['brand']
       name = request.form['name']
       release_date = request.form['release_date']
       disc_number = request.form['disc_number']
       abbreviation = request.form['abbreviation']
       cost = request.form['cost']

       # Check if product exists using MySQL
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM Item WHERE name = %s', (name,))
       item = cursor.fetchone()
       # If item exists show error and validation checks
       if item:
           msg = 'Item already exists!'
       elif not re.match(r'[A-Za-z0-9]+', brand):
           msg = 'Brand must contain only characters and numbers!'
       elif not re.match(r'[A-Za-z0-9]+', name):
           msg = 'Name must contain only characters and numbers!'
       elif not re.match(r'[0-9]+', release_date):
           msg = 'Release date must contain only numbers!'
       # elif not re.match(r'[0-9]+', disc_number):
       #   msg = 'Disc number must contain only numbers!'
       elif not re.match(r'[A-Za-z0-9]+', abbreviation):
           msg = 'Abbreviation must contain only characters and numbers!'
       elif not re.match(r'[0-9]+', cost):
           msg = 'Cost must contain only numbers!'
       elif not brand or not name or not release_date or not disc_number:
           msg = 'Please fill out the form!'
       else:
           # Item doesnt exists and the form data is valid, now insert new item into items table
           cursor.execute('INSERT INTO Item (brand, name, release_date, disc_number, abbreviation, cost) VALUES ( %s, %s, %s, %s, %s, %s)', (brand, name, release_date, disc_number, abbreviation, cost,))
           mysql.connection.commit()
           msg = 'Item successfully added'

   elif request.method == 'POST':
       # Form is empty... (no POST data)
       msg = 'Please fill out the form!'
   # Show registration form with message (if any)
   return render_template('addItem.html', msg=msg)


@app.route('/inventory.html', methods=['GET', 'POST'])
def inventory():
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cursor.execute('SELECT * FROM Item')
   data = cursor.fetchall()
   return render_template('inventory.html', output_data=data)


# Commented out as no register page yet
# @app.route('/register', methods=['GET', 'POST'])
# def adminRegister():
# Output message if something goes wrong...
#  msg = ''
# Check if "username", "password" and "email" POST requests exist (user submitted form)
# if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
# Create variables for easy access
#    email = request.form['email']
#   password = request.form['password']

# Check if account exists using MySQL
# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# cursor.execute('SELECT * FROM Admin WHERE email = %s', (email,))
# account = cursor.fetchone()
# If account exists show error and validation checks
# if account:
#   msg = 'Account already exists!'
# elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#  msg = 'Invalid email address!'
# elif not username or not password or not email:
# msg = 'Please fill out the form!'
#  else:
# Account doesnt exists and the form data is valid, now insert new account into accounts table
#      cursor.execute('INSERT INTO Admin (email, password) VALUES ( %s, %s)', (email, password,))
#       mysql.connection.commit()
#        msg = 'You have successfully registered!'

# elif request.method == 'POST':
#      # Form is empty... (no POST data)
#       msg = 'Please fill out the form!'
# Show registration form with message (if any)
#    return render_template('register.html', msg=msg)


# @app.route('/itemPage.html', methods=['GET', 'POST'])
# def itemPage() :
#     msg = ''
#    # Check if "item" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'Name' in request.form:
#         # Create variables for easy access
#         name = request.form['Name']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM Item WHERE Name = %s', (name,))
#         # Fetch one record and return result
#         product = cursor.fetchone()
#         # If account exists in accounts table in out database
#         if product:
#             # Create session data, we can access this data in other routes
#             session['Name'] = product['Name']
#             # Redirect to item's page
#             return redirect(url_for('itemPage'))
#     return render_template('itemPage.html', msg=msg)

# @app.route('/addItemToCart.html', methods=['GET', 'POST'])
# def addItemToCart() :
#     if request.method == 'POST' and 'product_Name' in regester.form and 'quantity' in request.form :
#         product_Name = request.form.get('product_Name')
#         quantity = request.form.get('quantity')
        
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM Item WHERE product_Name = %s', (product_Name,))
#         item = cursor.fetchone()


# @app.route('/order.html', methods=['GET', 'POST'])
# def showOrder() :



if __name__ == '__main__':
   app.run()
