from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user

from app.forms import RegistrationForm, LoginForm
from app.services import AuthService
from app.utils import Response

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        next_page = request.args.get('next')
        response: Response = AuthService.register_user(
            name=form.name.data,
            password=form.password.data,
            email=form.email.data,
        )
        if response.error_message:
            flash(response.error_message, response.error_category)
            return redirect(url_for(response.redirect_url or 'auth.register', next=next_page))
        login_user(response.data)
        return redirect(next_page or url_for('post.get_all_posts'))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        next_page = request.args.get('next')
        response: Response = AuthService.authenticate_user(email=form.email.data, password=form.password.data)
        if response.error_message:
            flash(response.error_message, response.error_category)
            return redirect(url_for('auth.login', next=next_page))
        login_user(response.data)
        return redirect(next_page or url_for('post.get_all_posts'))
    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('post.get_all_posts'))
