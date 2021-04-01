from flask import Flask, render_template, request 
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

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
        #Creating a connection cursor
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO seller_table VALUES(%s, %s,%s,%s)''', (first_name, last_name, email, password))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"

app.run(host='localhost', port= 5000)

#just adding this comment to show a change on git