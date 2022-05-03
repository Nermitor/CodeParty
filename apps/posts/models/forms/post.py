from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from data import db_session
from data.models.languages import Language



class PostForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    code = TextAreaField("Код", validators=[DataRequired()])
    language = SelectField("Язык", choices=[
        (lang.id, lang.full_name) for lang in db_session.create_session().query(Language).all()
    ])
    submit = SubmitField("Опубликовать")