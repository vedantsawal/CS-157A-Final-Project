from app import app
from flask import render_template, request, redirect, url_for, flash, jsonify
from .models import db, Cart, User, Products
from flask_login import current_user, login_required, login_user
from .auth.forms import AddProductsForm, MakeAdminForm
#from .apiauthhelper import basic_auth_required, token_auth_required
from werkzeug.security import check_password_hash

@app.before_first_request
def create_tables():
    #db.drop_all()
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    products = Products.query.all()
    return render_template('home.html', products = products)

@app.route('/showusers')
def show_users():
    users = User.query.all()
    return render_template('showusers.html', users=users)

@app.route('/<int:product_id>', methods=["GET"])
def getProduct(product_id):
    product = Products.query.get(product_id)
    return render_template('singleproduct.html', product=product)

@login_required
@app.route("/cart")
def cart():
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    products = []
    final_total = 0
    for item in cart_items:
        product = Products.query.get(item.product_id)
        product.quantity = item.quantity
        final_total += product.price * product.quantity
        products.append(product)
    return render_template('cart.html', cart=products, final_total = final_total)


@app.route('/<int:product_id>/add_to_cart', methods=["POST", "GET"])
def add_to_cart(product_id):

    if current_user.is_authenticated:
        user_id = current_user.id
        cart_item = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.saveToDB()
        else:
            cart = Cart(product_id=product_id, user_id=user_id, quantity=1)
            cart.saveToDB()
    else:
        flash('You need to log in to add items to your cart', category='danger')
        return redirect(url_for('auth.loginPage'))
    return redirect(url_for('cart'))

@app.route('/cart/<int:product_id>/remove', methods=["POST", "GET"])
def remove_from_cart(product_id):
    user_id = current_user.id
    cart_item = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()

    if not cart_item:
        return redirect(url_for('cart'))

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.saveToDB()
    else:
        cart_item.deleteFromDB()

    return redirect(url_for('cart'))

@app.route('/cart/clear', methods=["POST", "GET"])
def clear_cart():
    user_id = current_user.id
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    for cart_item in cart_items:
        cart_item.deleteFromDB()

    return redirect(url_for('cart'))

@app.route("/<int:product_id>/delete", methods=["POST", "GET"])
def deleteMug(product_id):
    product = Products.query.get(product_id)

    product.deleteFromDB()
    return redirect(url_for('home'))

@app.route("/addproducts", methods=["POST", "GET"])
def addProduct():
    if current_user.is_authenticated:
        if current_user.admin == True:
            form = AddProductsForm()
            products = Products.query.all()
            if request.method == "POST":
                if form.submit.data and form.validate():
                    title = form.title.data
                    img_url = form.img_url.data
                    caption = form.caption.data
                    price = form.price.data
                    quantity = form.quantity.data
                    
                    product = Products(title, img_url, caption, price, quantity)
                    product.saveToDB()
                    
                    flash("Successfully Added product to Database!", category='success')
                    return render_template('addproducts.html', form = form, products = products)
                else:
                    flash("Form didn't pass validation.", category='danger')
                    return render_template('addproducts.html', form = form, products = products)
                
            elif request.method == "GET":
                return render_template('addproducts.html', form = form, products = products)
        else:
            return render_template('addproducts.html', form = form, products = products)
    else:
        return render_template('addproducts.html', form = form, products = products)
            
@app.route("/makeadmin/<username>", methods=["POST", "GET"])
def MakeAdmin(username):
    user = User.query.filter_by(username=username).first()
    user.makeAdmin()
    return redirect(url_for('home'))

@app.route("/makeadmin/", methods=["POST", "GET"])
def MakeAdminPage():
    return render_template('makeadmin.html')


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 0 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
