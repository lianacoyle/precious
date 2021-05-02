from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///precious.db'
app.config['SECRET_KEY']='kjdshfkgjeiuvsdnvoasjs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, auto_increment="auto")
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    #vendor_flag = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())