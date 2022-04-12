from flask import render_template, flash
from flask_login import login_required

from core.token import generate_confirmation_token, confirm_token
from data import db_session
from data.models.users import User
from .app import authorisation
from .models.forms.register import RegisterForm


@authorisation.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    cur_template = "authorisation/index.html"
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template(cur_template, form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(cur_template, form=form, message="Аккаунт с этим email уже существует")
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template(cur_template, form=form, message="Аккаунт с таким именем уже существует")

        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        token = generate_confirmation_token(user.email)


@authorisation.route("/authorisation/token/<token>")
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('Ссылка для подтверждения истекла или неверна', 'danger')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first_or_404()
    if user.confirmed:
        flash("Аккаунт уже подтверждён. Войдите", "success")
    else:
        user.confirmed = True
        db_sess.commit()
        flash("Аккаунт был подтверждён.", "success")
    return ...
