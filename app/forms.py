"""File containing all forms used in the application"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User

class LocationForm(FlaskForm):
	"""Form used for the city search"""
	location = StringField('Location', validators=[DataRequired()])
	submit = SubmitField('Chercher le lieu')

class LoginForm(FlaskForm):
	"""Form used for loging"""
	email = StringField('Identifiant', validators=[DataRequired(), Email()])
	password = PasswordField('Mot de passe', validators=[DataRequired()])
	remember_me = BooleanField('Se souvenir de moi')
	submit = SubmitField('Connexion')

class RegistrationForm(FlaskForm):
	"""Form used for Registration"""
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_confirm = PasswordField('Password_confirm', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('S\'inscrire')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Cette adresse email est déjà utilisée.')
	