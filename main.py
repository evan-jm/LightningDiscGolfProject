from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from decimal import *
from werkzeug.utils import secure_filename
import os
import datetime
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sqlroot!'
app.config['MYSQL_DB'] = 'milestone2'
UPLOAD_FOLDER ='static/product-images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Intialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def Home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def Contact():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

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
        # Check if account Admin account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account, "admin table")

        # If account exists in accounts table in out database
        if account != None:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['ID'] = account['ID']
            session['username'] = account['username']
            session['user']=account
            # Redirect to home page
            return redirect("/adminHome/home/<session['user']>")

        # If account does not exist in Admin, check to see if credentials exist in User
        elif username != "mattm":
            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM User WHERE username = %s AND password = %s', (username, password,))
            # Fetch one record and return result
            account = cursor.fetchone()
            print(account, "85")
            # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['ID'] = account['ID']
                session['username'] = account['username']

                return redirect("/pythonlogin/home/<session['user']")

            else:
                session["message"] = "Incorrect username/password"

                message = ""
                if session.get("message"):
                    message = session.get("message")
                    session.pop("message", None)
                return render_template('login.html', message=message)


        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


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
        first_name = request.form['first_name']
        last_name = request.form['last_name']

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
            cursor.execute('INSERT INTO User (username, email, password,first_name,last_name) VALUES (%s,%s,%s,%s, %s)',
                           (username, email, password, first_name, last_name))
            mysql.connection.commit()
            session["message"] = 'You Have Successfully Registered!'
            return redirect("/register2")


    else:

        message = ""
        if session.get("message"):
            message = session.get("message")
            session.pop("message", None)

        return render_template('register.html', message=message)


# http://localhost:5000/pythinlogin/userHome - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def userHome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Admin WHERE username = %s', (session['username'],))
        account = cursor.fetchone()
        if account:
            return render_template('adminHome.html', user=session['user'])
        else:
            return render_template('userHome.html', user=session['user'])
    # User is not loggedin redirect to login page
    return redirect(url_for('userLogin'))


# http://localhost:5000/pythinlogin/adminHome - this will be the home page, only accessible for loggedin admins
@app.route('/adminHome/home')
def adminHome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('adminHome.html', user=session['user'])
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('userLogin'))


@app.route('/adminOrders.html', methods=['GET', 'POST'])
def viewOrdersAdmin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Orders')
    data = cursor.fetchall()
    return render_template('adminOrders.html', output_data=data)    


@app.route('/adminOrders.html/<string:id>', methods=['GET', 'POST'])
def cancelOrderAdmin(id):
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cursor.execute('DELETE FROM Order_Line_Item WHERE Order_ID = %s', (id,))
   mysql.connection.commit()
   cursor.execute('DELETE FROM Orders WHERE Order_ID = %s', (id,))
   mysql.connection.commit()
   return redirect(url_for('viewOrdersAdmin'))  


@app.route('/addItem', methods=['GET', 'POST'])
def addItem():
    # Output message if something goes wrong...
    msg = ''
    # Check if "brand", "name", "releaseDate", "discNumber", "abbreviation", and "cost" POST requests exist (user submitted form)
    if request.method == 'POST' and 'brand' in request.form and 'name' in request.form and 'release_date' in request.form and 'discType' in request.form and 'descrip' in request.form and 'cost' in request.form and 'image' in request.files:
        # Create variables for easy access
        brand = request.form['brand']
        name = request.form['name']
        release_date = request.form['release_date']
        discType = request.form['discType']
        descrip = request.form['descrip']
        cost = request.form['cost']
        image = request.files['image']
        itemCode = "None"

        # Check if product exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Item WHERE name = %s', (name,))
        item = cursor.fetchone()
        # If item exists show error and validation checks
        if item:
            msg = 'Item already exists!'
        elif not brand or not name or not release_date:
            msg = 'Please fill out the form!'
        else:
            # Item doesnt exists and the form data is valid, now insert new item into items table
            # Get name of image & save it to file directory
            imageName = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], imageName))
            saveName = imageName
            cursor.execute('INSERT INTO Item (itemid,image, brand, name, disctype, description, release_date, itemcode, cost) VALUES ( %s,%s, %s, %s, %s, %s, %s, %s, %s)', (None,saveName, brand, name, discType, descrip, release_date, itemCode, cost,))
            mysql.connection.commit()
            msg = 'Item successfully added'
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Brands WHERE BrandName = %s', (brand,))
            thisbrand = cursor.fetchone()
            if thisbrand is None:
                cursor.execute('INSERT INTO Brands (BrandName) VALUES (%s)', (brand,))
                mysql.connection.commit()

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM DiscTypes WHERE TypeName = %s', (discType,))
            type = cursor.fetchone()
            if type is None:
                cursor.execute('INSERT INTO DiscTypes (TypeName) VALUES (%s)', (discType,))
                mysql.connection.commit()

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('addItem.html', msg=msg)


@app.route('/updateItem/<string:id>', methods=['GET', 'POST'])
def updateItem(id):
    msg = ""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Item WHERE ItemID = %s', (id,))
    item = cursor.fetchone()

    #Valuecheck method checks if there is value to update, otherwise sets it to current value
    if request.method == 'POST' and 'brand' in request.form and 'name' in request.form and 'release_date' in request.form and 'discType' in request.form and 'descrip' in request.form and 'cost' in request.form:
        name = valueCheck(request.form['name'], item['Name'])
        brand = valueCheck(request.form['brand'], item['Brand'])
        date = valueCheck(request.form['release_date'], item['Release_Date'])
        type = valueCheck(request.form['discType'], item['DiscType'])
        descrip = valueCheck(request.form['descrip'], item['Description'])
        cost = valueCheck(request.form['cost'], item['Cost'])
        itemCode = valueCheck(request.form['code'],item['ItemCode'])
        try:
            image= request.files['image'] if 'image' in request.files else None
            imageName = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], imageName))
        except:
            imageName=item['Image']

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE Item SET image=%s, brand=%s, name=%s, disctype=%s, description=%s, release_date=%s, itemcode=%s, cost=%s WHERE ItemID=%s', (imageName, brand, name, type, descrip, date, itemCode, cost, id))
            mysql.connection.commit()
            msg = 'Item successfully updated'
        except:
            msg = 'Error!  Looks like there was a problem...try again!'
            render_template('updateItem.html', id=id, msg=msg,item=item)
    return render_template('updateItem.html', id=id, msg=msg, item=item)


def valueCheck(field, itemfield):
    if field=="":
        field=itemfield
    return field


@app.route('/inventory.html/<string:id>', methods=['GET', 'POST'])
def deleteItem(id):
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cursor.execute('DELETE FROM Item WHERE ItemID = %s', (id,))
   mysql.connection.commit()
   return redirect(url_for('inventory'))    

@app.route('/inventory.html', methods=['GET', 'POST'])
def inventory():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Item')
    data = cursor.fetchall()
    return render_template('inventory.html', output_data=data)


@app.route('/orders.html', methods=['GET', 'POST'])
def viewOrdersUser():
    id=str(session['ID'])
    print(id)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Orders WHERE User_ID=%s',[id])
    data = cursor.fetchall()
    return render_template('orders.html', output_data=data)    


@app.route('/orders.html/<string:id>', methods=['GET', 'POST'])
def cancelOrder(id):
   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
   cursor.execute('DELETE FROM Order_Line_Item WHERE Order_ID = %s', (id,))
   mysql.connection.commit()
   cursor.execute('DELETE FROM Orders WHERE Order_ID = %s', (id,))
   mysql.connection.commit()
   return redirect(url_for('viewOrdersUser'))  


@app.route('/userHome/<string:id><string:userType>', methods=['GET', 'POST'])
def updateUser(id,userType):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if userType == "User":
        cursor.execute('SELECT * FROM User WHERE ID = %s', (id,))
    else:
        cursor.execute('SELECT * FROM Admin WHERE ID = %s', (id,))
    account= cursor.fetchone()
    if request.method == "POST" and account:
        updateFirstName = request.form['firstname']
        updateLastName= request.form['lastname']
        updateEmail = request.form['email']
        updateUsername = request.form['username']
        updatePword= request.form['password']

        #Check if username already exists
        cursor.execute('SELECT * FROM User WHERE ID = %s', (id,))
        checkAccount= cursor.fetchone()
        if checkAccount and checkAccount['username'] != account['username']:
            msg='Username Already Exists!'
            return render_template("userHome.html", msg=msg,user=account)
        else:
            cursor.execute('UPDATE User SET username=%s, first_name=%s, last_name=%s, email=%s, password=%s WHERE ID=%s', (updateUsername,updateFirstName,updateLastName,updateEmail,updatePword,id))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM User WHERE ID = %s', (id,))
            account= cursor.fetchone()
            return render_template("userHome.html", user=account)

#Will be moved, method for viewing products
@app.route('/products.html',methods=['GET', 'POST'])
def products():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Item')
    rows= cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands')
    all_brands = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes')
    all_types = cursor.fetchall()

    return render_template('products.html',items=rows, brands=all_brands, disc_types=all_types)


@app.route('/brand/<int:ID>',methods=['GET', 'POST'])
def get_brand(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands WHERE Brand_ID = %s', (ID,))
    brand = cursor.fetchone()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands')
    all_brands = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT BrandName FROM Brands WHERE Brand_ID = %s', (ID,))
    brandName = cursor.fetchone()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_list = list(brandName.values())
    extracted_Brand_Name = my_list[0]
    cursor.execute('SELECT * FROM Item WHERE Brand = %s', (extracted_Brand_Name,))
    brandsort = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes')
    all_types = cursor.fetchall()

    return render_template('products.html', brand = brand, brands = all_brands, brandsort = brandsort, disc_types=all_types)


@app.route('/type/<int:ID>',methods=['GET', 'POST'])
#@app.route('/products/brand/<int:ID>',methods=['GET', 'POST'])
def get_type(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes WHERE Type_ID = %s', (ID,))
    type = cursor.fetchone()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes')
    all_types = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT TypeName FROM DiscTypes WHERE Type_ID = %s', (ID,))
    typeName = cursor.fetchone()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    my_list = list(typeName.values())
    extracted_Type_Name = my_list[0]
    cursor.execute('SELECT * FROM Item WHERE DiscType = %s', (extracted_Type_Name,))
    typesort = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands')
    all_brands = cursor.fetchall()

    return render_template('products.html', type = type, disc_types=all_types, typesort = typesort, brands = all_brands)


@app.route('/products/search', methods=['GET', 'POST'])
def search():

    msg = None

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands')
    all_brands = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes')
    all_types = cursor.fetchall()

    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Item WHERE Brand LIKE %s OR DiscType LIKE %s OR Name LIKE %s', (search, search, search))
        data = cursor.fetchall()

        if data == ():
            msg = 'sorry, no matches'

        return render_template('products.html', msg =msg, items=data, brands=all_brands, disc_types=all_types)
    else:
        return redirect(url_for('products'))


@app.route('/products/hightolow', methods=['GET', 'POST'])
def hightolow():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands')
    all_brands = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes')
    all_types = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Item ORDER BY CAST(Cost AS DECIMAL(10, 2)) DESC')
    hightolow = cursor.fetchall()

    return render_template('products.html', items=hightolow, brands=all_brands, disc_types=all_types)


@app.route('/products/lowtohigh', methods=['GET', 'POST'])
def lowtohigh():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Brands')
    all_brands = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DiscTypes')
    all_types = cursor.fetchall()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Item ORDER BY CAST(Cost AS DECIMAL(10, 2)) ASC')
    lowtohigh = cursor.fetchall()

    return render_template('products.html', items=lowtohigh, brands=all_brands, disc_types=all_types)


@app.route('/cart.html', methods=['GET', 'POST'])
def showCart():
    return render_template('cart.html',msg='')


#Method for adding project to cart, uses array for each thing
@app.route('/add', methods=['POST'])
def add_product_to_cart():
    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        # validate the received values
        if request.method=='POST':
            _quantity = int(request.form['quantity'])
            _code = request.form['code']
            # validate the received values
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM Item WHERE ItemCode=%s', (_code,))
            row = cursor.fetchone()

            costStr=row['Cost']
            cost= Decimal(costStr)
            itemArray = {row['ItemCode']: {'Name': row['Name'], 'ItemCode': row['ItemCode'], 'quantity': _quantity, 'Cost': cost, 'Image': row['Image'], 'total_price': _quantity * cost}}

            all_total_price = 0
            all_total_quantity = 0

            session.modified = True
            if 'cart_item' in session and session['cart_item'] != "":
                if row['ItemCode'] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if row['ItemCode'] == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * cost
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * cost

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            return redirect(url_for('products'))
        else:
            return 'Error while adding item to cart'
    except Exception as e:
      print("error adding!\n",e)
    finally:
        try:
            cursor.close()
        except Exception as e:
            print("error closing!\n",e)


#Method to empty the cart
@app.route('/empty')
def empty_cart():
    try:
        session['cart_item']=""
        return redirect(url_for('.showCart'))
    except Exception as e:
        print(e)


#Method to delete product from the cart
@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                break

        if all_total_quantity == 0:
            session['cart_item']=""
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return redirect(url_for('.showCart'))
    except Exception as e:
        print(e)


#Method to merge arrays of items
def array_merge( first_array , second_array ):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False


@app.route('/products/<string:id>')
def single_item_page(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Item WHERE ItemID= %s',(id,))
    item= cursor.fetchone()
    return render_template('singleProd.html',item=item)


#Method to show checkout page
@app.route('/cart', methods=['GET','POST'])
def checkoutPage():
    if 'shipMethod' in request.form and request.method=='POST':
        if request.form['shipMethod']== "Bubble Mailer":
            total=Decimal(session['all_total_price'])+2
            shipCost="$2.00"
        elif request.form['shipMethod'] == "Collector's Bag":
            total=Decimal(session['all_total_price'])+4
            shipCost="$4.00"
        else:
            total=total=Decimal(session['all_total_price'])+6
            shipCost="$6.00"

        if 'loggedin' in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM User WHERE username=%s', (session['username'],))
            user= cursor.fetchone()
        else:
            user=None
        return render_template('checkout.html',user=user,total=total,ship=request.form['shipMethod'],shipCost=shipCost)
    else:
        return render_template('cart.html',msg='Please select a shipping method!')
    

#Method to checkout & create order from the cart
@app.route('/checkout',methods=['GET','POST'])
def checkout():
    if request.method=='POST' and 'email' in request.form and 'lastname' in request.form and 'firstname' in request.form and 'address' in request.form:
        total=Decimal(request.form['newTotalPrice'])
        quantityT= session['all_total_quantity']
        email = request.form['email']
        fname = request.form['firstname']
        lname = request.form['lastname']
        ship= request.form['address']
        
        #Checks id of last order, increments it for new order
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #Check if user logged into account, then just create order off their info    
        if 'loggedin' in session:
            cursor.execute('INSERT INTO Orders(order_id,order_date,user_id,guest_id,address,order_total,total_quantity) VALUES (%s,%s,%s,%s,%s,%s,%s)', (None,datetime.datetime.now(),session['ID'],None,ship,total,quantityT,))
            mysql.connection.commit()
        #Else create guest, then create order based off of their info 
        else:
            time= datetime.datetime.now()
            cursor.execute('INSERT INTO Guest(id,first_name,last_name,email,use_time) VALUES (%s,%s,%s,%s,%s)', (None,fname,lname,email,time,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM Guest ORDER BY ID DESC LIMIT 1')
            lastGuest= cursor.fetchone()
            currGuest= lastGuest['ID']
            cursor.execute('INSERT INTO Orders(order_id,order_date,user_id,guest_id,address,order_total,total_quantity) VALUES (%s,%s,%s,%s,%s,%s,%s)', (None,datetime.datetime.now(),None,currGuest,ship,total,quantityT,))
            mysql.connection.commit()
        #Next add each item in cart into order_line_item
        cursor.execute('SELECT * FROM Orders ORDER BY Order_ID DESC LIMIT 1')
        lastOrder= cursor.fetchone()
        currOrder= lastOrder['Order_ID']
        for item in session['cart_item'].items():
            quantity= session['cart_item'][item[0]]['quantity']
            itemTotal= Decimal(session['cart_item'][item[0]]['total_price'])
            cursor.execute('SELECT * FROM Item WHERE ItemCode=%s',(session['cart_item'][item[0]]['ItemCode'],))
            itemID=cursor.fetchone()
            cursor.execute('INSERT INTO Order_Line_Item(order_id,itemid,product_quantity,cost_total) VALUES (%s,%s,%s,%s)',(currOrder,int(itemID['ItemID']),quantity,itemTotal,))
            mysql.connection.commit()
        session['cart_item']=""
        return redirect(url_for('showCart'))
    else:
        return render_template('checkout.html',msg='Please enter 1 or more missing fields!')


if __name__ == '__main__':
    app.run()
