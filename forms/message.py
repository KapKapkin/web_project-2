from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SendMessageForm(FlaskForm):
    text = TextAreaField('Введите текст', validators=[DataRequired()])
    submit = SubmitField('Отправить')