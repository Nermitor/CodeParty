from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    repeat_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    email = EmailField("Ваш email", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
