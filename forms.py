from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
#from wtforms import DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange


class Top_States_Form(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=1, max=20)])
    amount = IntegerField('How many states?', validators=[DataRequired(), NumberRange(1, 50)])
    starting_date = DateField('Starting Date', format="%Y-%m-%d",validators=[DataRequired()])
    submit = SubmitField('Submit')

#https://mrl33h.de/post/21
#https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/03-Forms-and-Validation
