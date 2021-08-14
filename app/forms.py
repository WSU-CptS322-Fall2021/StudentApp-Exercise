from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  ValidationError, Length
from app.models import Class

class ClassForm(FlaskForm):
    coursenum = StringField('Course Number',[Length(min=3, max=3)])
    submit = SubmitField('Post')
