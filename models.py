import datetime
from flask import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the database models
class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    DateOfBirth = db.Column(db.Date)
    Address = db.Column(db.String(255))
    City = db.Column(db.String(50))
    State = db.Column(db.String(50))
    ZipCode = db.Column(db.String(10))
    Country = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(20))
    DateOfRegistration = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class OAuth2Client(db.Model):
    __tablename__ = 'oauth2client'
    client_id = db.Column(db.String(48), primary_key=True)
    client_secret = db.Column(db.String(120), nullable=False)
    client_metadata = db.Column(db.Text, nullable=False)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))

class OAuth2Token(db.Model):
    __tablename__ = 'oauth2token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.String(48), db.ForeignKey('oauth2client.client_id'))
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True, nullable=True)  # Allow NULL values
    refresh_token = db.Column(db.String(255), unique=True)
    scope = db.Column(db.Text)
    revoked = db.Column(db.Boolean, default=False)
    issued_at = db.Column(db.Integer)
    expires_in = db.Column(db.Integer)
    access_token_revoked_at = db.Column(db.Integer, nullable=True)  # Allow NULL values
    refresh_token_revoked_at = db.Column(db.Integer, nullable=True)  # Allow NULL values
