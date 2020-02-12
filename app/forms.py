from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    inp = StringField('Podaj nazwę artykułu', validators=[DataRequired()])
    submit = SubmitField('Go')