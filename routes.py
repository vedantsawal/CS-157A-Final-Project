from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import User
from .forms import UserCreationForm, LoginForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            phone_number = form.phone_number.data
            address = form.address.data
            
            # add user to database
            user = User(username, password, first_name, last_name, phone_number, address)

            user.saveToDB()

            return redirect(url_for('auth.loginPage'))

    return render_template('signup.html', form = form )

@auth.route('/login', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            # check is user with that username even exists
            user = User.query.filter_by(username=username).first()
            if user:
                #if user ecxists, check if passwords match
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash(f'Successfully logged in! Welcome back {user.username}', category='success')                    
                    return redirect(url_for('home'))
                else:
                    flash('wrong password', category='danger')
            else:
                flash('user doesnt exist', category='danger')

    return render_template('login.html', form = form)

@auth.route('/logout', methods=["GET"])
@login_required
def logoutRoute():
    logout_user()
    return redirect(url_for('auth.loginPage'))