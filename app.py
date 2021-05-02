#run in cmd terminal: 
# python -m pip install {library name}


from flask import Flask, render_template, request, redirect, flash, session
import os
from flask import  url_for 
from werkzeug.utils import secure_filename
from config import *
import sys,os,re  
#i have added the above imports (Sandra)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

from forms import RegistrationForm, LoginForm


UPLOAD_FOLDER = 'static/imgs'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
count = 0
app = Flask(__name__)
app.secret_key = "secret"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
#app.config['SLQALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 


class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #vendor_flag = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    items = db.relationship('Item', backref='user', lazy=True)
    carts = db.relationship('Cart', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User('{self.userid}','{self.first_name}','{self.last_name}')"

class Category(db.Model):
    categoryid = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    category_name = db.Column(db.String(100), nullable=False)
    category_desc = db.Column(db.String(255), nullable=False)

    def __init__(self, category_name, category_desc):
        self.category_name = category_name
        self.category_desc = category_desc

    def __repr__(self):
        return f"Category: '{self.category_name}' /n", \
            f"Description: '{self.category_desc}' /n"


class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(7,2), nullable=False)
    #create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable=False)

    cartdetails = db.relationship('CartDetails', backref='item', lazy=True)

    # note: defaults to '1' for category id and user id
    def __init__(self, item_name, filename, item_desc, price, userid=1, categoryid=1):
        self.item_name = item_name
        self.filename = filename
        self.item_desc = item_desc
        self.price = price
        self.userid = userid
        self.categoryid = categoryid

    def __repr__(self):
        return f"Item('{self.itemid}','{self.item_name}','{self.filename}','{self.price}')"


class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #update_time = db.Column(db.DateTime, nullable=True)
    userid = db.Column(db.DateTime, db.ForeignKey('user.userid'), nullable=True)

    def __init__(self, userid=0):
        self.userid = userid

    def __repr__(self):
        return f"Cart ID: {{self.cartid}}/n",\
                "Create Time: {{self.create_time/n"


class CartDetails(db.Model):
    cartdetailsid = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    cartid = db.Column(db.Integer, db.ForeignKey('cart.cartid'), nullable=False)
    itemid = db.Column(db.Integer, db.ForeignKey('item.itemid'), nullable=False)

    def __init__(self, itemid, quantity, cartid):
        #checking to see if Cart by cartid already exists
        cart = Cart.query.filter_by(cartid=cartid).first()
        if cart is None:
            cart = Cart()
        else:
            cartid = cart.cartid

        self.itemid = itemid
        self.quantity = quantity


#root/home page
@app.route("/")
@app.route("/precious")
def precious():
    return render_template('home.html')

@app.route('/DevPage')
def DevPage():
    return render_template('Dev_Page.html')

@app.route("/phot")
def phot():
    return "Photography"

@app.route("/contact")
def contact():
    return render_template('Contactus.html')

@app.route("/me")
def me():
    return "PM"


@app.route("/des")
def designs():
    return "Des"

@app.route('/shopping')
def shopping():
    return render_template('shopping.html', items=Item.query.all())

@app.route('/shopping/<itemid>')
def showItem(itemid):
    item = Item.query.filter_by(itemid=itemid).first()
    return render_template('itemPage.html', item=item)

@app.route('/cart/<cartid>')
def showCart(cartid):
    return render_template('cart.html')


# Create new user account
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if not request.form['fname'] or not request.form['lname'] or not request.form['uname']\
        or not request.form['email'] or not request.form['pword']:
            flash('Please enter all the fields', 'error')
        else:
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            username = request.form["uname"]
            email = request.form["email"]
            password = request.form["pword"]
            password_check = request.form["cpword"]
            print('form entries')
            '''
            found_user = User.query.filter_by(email=email).first()
            if found_user:
                flash("Account for that email already exists!")
                return redirect(url_for("login"))
    
            else:
            '''
            usr = User(first_name, last_name, email, username, password)
            print('object instantiated')
            db.session.add(usr)
            db.session.commit()
            print('user object committed')
            print(usr)
            flash("Account successfully created!")
            return redirect(url_for("viewUsers"))

    return render_template('createAccount.html')

@app.route("/viewUsers")
def viewUsers():
    return render_template('viewUsers.html', values=User.query.all())


@app.route("/profile")
def profile():
    return "profile"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thank you for registering','success')
        return redirect(url_for('precious'))
    return render_template('register.html', form=form, title="Registration page")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method =="POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} You are logged in now', 'success')
            return redirect(request.args.get('next') or url_for('precious'))
        else:
            flash ('Wrong Password please try again', 'danger')

    return render_template('login.html', form=form, title="Login Page")


@app.route("/logout")
def logout():
    return "You have completed a successful logout!"

# user checkout page
@app.route("/ucos")
@app.route("/userCheckout")
def uco():
    return render_template('userCheckout.html')

# user upload page

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uua") 
@app.route('/userUpload')
def upload_form():
    return render_template('userUpload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            item_name = request.form["title"]
            item_fname = file.filename
            item_desc = request.form["description"]
            item_price = float(request.form["price"])

            item = Item(item_name, item_fname, item_desc, item_price)
            db.session.add(item)
            db.session.commit()
            print('item object committed')
            flash("Item successfully created!")
            return redirect(url_for("viewItems"))

            #return redirect(url_for('upload_form',filename=filename))
    return "Congratulations Upload Complete"

@app.route("/viewItems")
def viewItems():
    return render_template('viewItems.html', values=Item.query.all())

#     '''
#   #  <!doctype html>
#   #  <title>Upload new File</title>
#    # <h1>Upload new File</h1>
#    # <form method=post enctype=multipart/form-data>
#     #  <input type=file name=file>
#     #  <input type=submit value=Upload>
#    # </form>
# '''

# shopping cart page
@app.route("/scn") 
@app.route('/shoppingCart')
def upload_cart():
    return render_template('shoppingCart.html')
          
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

app.run(host='localhost', port=5000)
