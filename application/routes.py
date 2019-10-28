from flask import current_app as app
from flask import render_template, flash, redirect, url_for

from .models import User, Chat, Message
from application.users.routes import UserAPI
from application.users.authentication import RegistrationForm, LoginForm
from application.messages.routes import MessageAPI
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

app.register_blueprint(UserAPI, url_prefix='/api/users')
app.register_blueprint(MessageAPI, url_prefix='/api/chats')

# homepage
@app.route('/')
@app.route('/index')
@login_required
def welcome():
    return render_template('home.html')

# registration
@app.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    )

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

#Logout Route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
