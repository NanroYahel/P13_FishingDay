from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
	location = StringField('Location', validators=[DataRequired()])
	submit = SubmitField('Chercher le lieu')