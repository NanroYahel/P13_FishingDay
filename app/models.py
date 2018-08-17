"""Contain the models for the database"""

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login



class User(UserMixin, db.Model):
    """Class representing an user"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(130))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """Generate an hash to save password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the hash of the password with the hash in db"""
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """Use by the user for connexion"""
    return User.query.get(int(id))

class City(db.Model):
    """Class used to stock the cities searched by users"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)


class UserSearch(db.Model):
    """Class used to stock the searches for an user"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    count = db.Column(db.Integer, index=True)
