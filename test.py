import app

db.connect()
user1 = user(first_name='Some', last_name='One', email='mail', password='password', vendor_flag=True)
db.session.add(user1)
db.session.commit()