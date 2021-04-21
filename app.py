#run in cmd terminal: 
# python -m pip install flask-sqlalchemy
# python -m pip install pymysql
# python -m pip install Pillow


from flask import Flask, render_template, request, redirect, flash, url_for
from flask import Flask, render_template, request, redirect
import os

class Item:
    def __init__(self, photo_name, price, file_name, category=None, item_desc=None):
        self.item_name = photo_name
        self.category = category
        self.item_desc = item_desc
        self.price = price
        self.file_name = file_name
        self.tn_file_name = None


#creating an empty list for Photo objects
items = []

#instantiating Photo objects and adding them to list of photos
pic1 = Item("Paper Lantern Alley", 10.00, 'pic1.jpg', '', "Some interesting description here")
items.append(pic1)
pic2 = Item("Rainy Street Glimmer", 15.00, 'pic2.jpg')
items.append(pic2)
pic3 = Item("Tax Free Night Sign", 12.00, 'pic3.jpg')
items.append(pic3)
pic4 = Item("Baby Pandas", 11.00, 'pic4.jpg')
items.append(pic4)
pic5 = Item("Pink Sky Mountain", 16.00, 'pic5.jpg')
items.append(pic5)


from werkzeug.utils import secure_filename


class Item:
    def __init__(self, photo_name, price, file_name, category=None, item_desc=None):
        self.item_name = photo_name
        self.category = category
        self.item_desc = item_desc
        self.price = price
        self.file_name = file_name
        self.tn_file_name = None


#creating an empty list for Photo objects
items = []

#instantiating Photo objects and adding them to list of photos
pic1 = Item("Paper Lantern Alley", 10.00, 'pic1.jpg', '', "Some interesting description here")
items.append(pic1)
pic2 = Item("Rainy Street Glimmer", 15.00, 'pic2.jpg')
items.append(pic2)
pic3 = Item("Tax Free Night Sign", 12.00, 'pic3.jpg')
items.append(pic3)
pic4 = Item("Baby Pandas", 11.00, 'pic4.jpg')
items.append(pic4)
pic5 = Item("Pink Sky Mountain", 16.00, 'pic5.jpg')
items.append(pic5)


app = Flask(__name__)

#root/home page
@app.route("/")
@app.route("/precious")
def precious():
	return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

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
    return render_template('shopping.html', items=items)

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

app.run(host='localhost', port= 5000)
