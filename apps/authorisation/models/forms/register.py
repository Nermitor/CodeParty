from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    email = EmailField("Ваш email", validators=[DataRequired()])
    about = TextAreaField("Расскажите о себе")
    languages = StringField("Какими языками программирования/технологиями вы владеете?")
    submit = SubmitField("Зарегистрироваться")
