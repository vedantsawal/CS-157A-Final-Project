from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from secrets import token_hex
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    address = db.Column(db.String(255))
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, first_name, last_name, phone_number, address):
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
        
    def makeAdmin(self):
        self.admin = True
        db.session.commit()
        
    def to_dict(self):
        return {"id": self.id, 
                "Username": self.username, 
                "Phone Number": self.phone_number,
                "First Name": self.first_name,
                "Last Name": self.last_name,
                "Address": self.address
                }

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(1000))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, title, img_url, caption, price, quantity):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.price = price
        self.quantity = quantity

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
        
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
        
    def to_dict(self):
        return {"id": self.id, 
                "title": self.title, 
                "img_url": self.img_url, 
                "caption": self.caption, 
                "price": self.price, 
                "quantity": self.quantity}

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __init__(self, user_id, product_id, quantity=1):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def update_quantity(self, quantity):
        self.quantity += quantity
        db.session.commit()

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

class Order_Details(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float)
    payment_id = db.Column(db.Integer)

    def __init__(self, user_id, total, payment_id):
        self.user_id = user_id
        self.total = total
        self.payment_id = payment_id

    def __repr__(self):
        return '<Order_Details %r>' % self.name
    
class Order_Items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<Order_Items %r>' % self.name
'''    
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer, db.ForeignKey('Order_Items.id'), nullable=False)
    amount = db.Column(db.Float)
    provider = db.Column(db.String(255))
    status = db.Column(db.String(255))

    def __init__(self, order_id, amount, provider, status):
        self.order_id = order_id
        self.amount = amount
        self.provider = provider
        self.status = status

    def __repr__(self):
        return '<Invoice %r>' % self.name
'''        
if __name__ == '__main__':
    db.create_all()