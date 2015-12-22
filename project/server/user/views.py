# project/server/user/views.py


###########
# imports #
###########

from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from sqlalchemy import exc

from project.server import bcrypt, db
from project.server.models import User, Student
from project.server.user.forms import LoginForm, RegisterForm, PasswordForm

##########
# config #
##########

user_blueprint = Blueprint('user', __name__,)


##########
# routes #
##########

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = Student(
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Thank you for registering.', 'success')
            return redirect(url_for("main.home"))
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect(url_for("main.home"))

    return render_template('user/register.html', form=form)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']
        ):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', title='Please Login', form=form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    form = PasswordForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        user.password = bcrypt.generate_password_hash(form.password.data)
        try:
            db.session.commit()
            flash('Password Updated!', 'success')
            return redirect(url_for('main.home'))
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect(url_for('main.home'))
    return render_template('user/password.html', form=form)
