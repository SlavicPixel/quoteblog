from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class QuoteForm(FlaskForm):
    author_guess = StringField('Your Guess:', validators=[DataRequired()])
    submit = SubmitField('Guess') 