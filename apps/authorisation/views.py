from flask import render_template, flash, url_for, redirect
from flask_login import login_user

from core.mailing.mail import MailMessage
from core.token import generate_confirmation_token, confirm_token
from data import db_session
from data.models.users import User
from .app import authorisation
from .models.forms.login import LoginForm
from .models.forms.register import RegisterForm


@authorisation.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    cur_template = "authorisation/register.html"
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template(cur_template, form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(cur_template, form=form, message="Аккаунт с этим email уже существует")

        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            about=form.about.data,
            languages=form.languages.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for("authorisation.confirm_email", token=token, _external=True)
        template = render_template("authorisation/confirm_email_mail.html", confirm_url=confirm_url)
        title = "Please confirm your email"
        mail = MailMessage(
            title=title,
            recipients=[user.email],
            template=template
        )
        mail.send()
        flash('A confirmation email has been sent via email.', 'success')
        return "OK"

    return render_template("authorisation/register.html", form=form)


@authorisation.route("/authorisation/token/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('Ссылка для подтверждения истекла или неверна', 'danger')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user:
        if user.confirmed:
            flash("Аккаунт уже подтверждён. Войдите", "success")
        else:
            user.confirmed = True
            db_sess.commit()
            flash("Аккаунт был подтверждён.", "success")
            login_user(user)
        return redirect('/profile')


@authorisation.route("/login", methods=['POST', "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

    return render_template("authorisation/login.html", form=form)
