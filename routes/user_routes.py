from flask import Blueprint, render_template, redirect, url_for, flash, request, get_flashed_messages
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.base import db
from forms.login import LoginForm, RegisterForm

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash("Email already exists.")
            return redirect(url_for("user.register"))

        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        new_user = User(email=email, name=name, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("main.homepage"))
    return render_template("auth/register.html", form=form, msg=get_flashed_messages())

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials")
            return redirect(url_for("user.login"))
        
        login_user(user)
        return redirect(url_for("main.homepage"))
    return render_template("auth/login.html", form=form, msg=get_flashed_messages())

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))
