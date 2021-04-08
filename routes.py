import sys,os,re  
from flask import Flask, session, render_template, request, redirect, url_for 
from werkzeug.utils import secure_filename
from config import *
#from flask_mysqldb import MySQL
UPLOAD_FOLDER = '/Users/sandr/Desktop/programs/uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
@app.route("/precious")
def precious():
	return render_template('home.html')

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
	
@app.route("/shop")
def shopping():
	return "shop"
	
@app.route("/profile")
def profile():
	return "profile"

@app.route("/login")
def login():
	return render_template('login.html')

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

@app.route('/uploader', methods = ['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_form',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# shooping cart page
@app.route("/scn") 
@app.route('/shoppingCart')
def upload_cart():
	return render_template('shoppingCart.html')
          


if __name__ == '__main__':
		app.run(debug=True)

app.run(host='localhost', port =5000)
