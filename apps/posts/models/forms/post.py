from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    code = TextAreaField("Код", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")