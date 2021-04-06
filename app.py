#run in cmd terminal: 
# python -m pip install flask-sqlalchemy
# python -m pip install pymysql
# python -m pip install Pillow


from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
import pymysql
#from PIL import image 
import os

app = Flask(__name__)

#Database attributes for connection
# will move credentials to separate config file later 
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format('root', '','localhost','precious')
app.config['SQLALCHEMY_DATABASE_URI'] = conn 
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']

#SQLAlchemy class definitions for each table using ORM (Object Relational Mapping)
#Columns defined here MUST match have matching attributes to database columns

class User(db.Model):
    iduser = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    vendor_flag = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, nullable=True)

#Example of instantiating a user object/record and adding it to the database
user1 = User(iduser=1001, first_name='Some', last_name='One', email='mail', password='password', vendor_flag=True)
db.session.add(user1)
db.session.commit()

'''
class item(db.Model):
    iditem = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    item_name = db.Column(db.String(100), nullable=False)
    idcategory = db.Column(db.Integer, db.ForeignKey('category.idcategory'), nullable=False)
    item_desc = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(7,2), nullable=False)
    create_time = db.Column(db.DateTime, nullable=True)

def convertToBinary(filename):
    with open(filename, 'rb') as file:
        binarydata=file.read()
    return binarydata

def convertBinaryToFile(binarydata, filename):
    with open(filename, 'wb') as file:
        file.write(binarydata)

    

class cart(db.Model):
    idcart = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=True)
    update_time = db.Column(db.DateTime, nullable=True)
    iduser = db.Column(db.DateTime, db.ForeignKey('user.iduser'), nullable=True)


class item(db.Model):
    idcartdetails = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    extended_price = db.Column(db.Numeric(7,2), nullable=False)
    idcart = db.Column(db.Integer, db.ForeignKey('cart.idcart'), nullable=False)
    iditem = db.Column(db.Integer, db.ForeignKey('item.iditem'), nullable=False)


class category(db.Model):
    idcategory = db.Column(db.Integer, primary_key=True)    
    category_name = db.Column(db.String(100), nullable=False)
    category_desc = db.Column(db.String(255), nullable=False)
'''





#

#root/home page
@app.route("/")
def start():
    return "Yay! It's working!"


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login form"

    if request.method == 'POST':
        first_name = request.form['First Name']
        last_name = request.form['Last Name']
        email = request.form['Email']
        password = request.form['Password']
        confirmPassword = request.form['Confirm Password']
        #Creating a connection cursor
        cursor = db.connection.cursor()
        cursor.execute(''' INSERT INTO seller_table VALUES(%s, %s,%s,%s)''', (first_name, last_name, email, password))
        db.connection.commit()
        cursor.close()
        return f"Done!!"

app.run(host='localhost', port= 5000)

#just adding this comment to show a change on git