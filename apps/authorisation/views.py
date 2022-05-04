from flask import render_template, flash, url_for, redirect, request
from flask_login import login_user

from app_settings import app
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
        with db_session.create_session() as db_sess:
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template(cur_template, form=form, message="Аккаунт с этим email уже существует")

            user = User(
                email=form.email.data,
                nickname=form.nickname.data,
                about=form.about.data,
                languages=form.languages.data
            )

            if form.avatar.data:
                on_form_name = form.avatar.name
                raw_name = form.avatar.data.filename
                if user.verify_ext(raw_name):
                    img = request.files[on_form_name].read(app.config['MAX_CONTENT_LENGTH'])
                    user.set_avatar(img)

            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            token = generate_confirmation_token(user.email)
            confirm_url = url_for("authorisation.confirm_email", token=token, _external=True)
            mail = MailMessage(
                title="Please confirm your email",
                recipients=[user.email],
                template=render_template("authorisation/confirm_email_mail.html", confirm_url=confirm_url)
            )
        mail.send()
        return render_template("authorisation/mail_is_send.html", email=user.email)

    return render_template("authorisation/register.html", form=form)


@authorisation.route("/authorisation/token/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return 'Ссылка для подтверждения истекла или неверна'
    with db_session.create_session() as db_sess:
        user = db_sess.query(User).filter(User.email == email).first()
        if user:
            if user.confirmed:
                return "Аккаунт уже подтверждён. Войдите"
            else:
                user.confirmed = True
                db_sess.commit()
                login_user(user)
            return redirect('/profile')


@authorisation.route("/login", methods=['POST', "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
            else:
                return render_template("authorisation/login.html", form=form, message='Неправильный пароль или почта')
        return redirect('/profile')

    return render_template("authorisation/login.html", form=form)
