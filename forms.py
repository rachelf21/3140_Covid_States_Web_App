from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
#from wtforms import DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, NumberRange


class Top_States_Form(FlaskForm):
    amount = IntegerField('How many states?', validators=[DataRequired(), NumberRange(min=1, max=50, message='cannot be greater than 50')])
    starting_date = DateField('Starting Date', format="%Y-%m-%d",validators=[DataRequired()],render_kw={'readonly': False})
    submit = SubmitField('Submit')

