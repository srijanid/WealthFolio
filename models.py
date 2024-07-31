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

class Category(db.Model):
    __tablename__ = 'categories'
    CategoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), nullable=False, unique=True)
    Description = db.Column(db.String(255))
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    TransactionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('Users.UserId'))
    CategoryId = db.Column(db.Integer, db.ForeignKey('Categories.CategoryId'))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    TransactionDate = db.Column(db.Date, nullable=False)
    Description = db.Column(db.String(255))
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class BillPayment(db.Model):
    __tablename__ = 'billpayments'
    BillId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('Users.UserId'))
    TransactionId = db.Column(db.Integer, db.ForeignKey('Transactions.TransactionId'))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    Due_date = db.Column(db.Date, nullable=False)
    Paid_date = db.Column(db.Date)
    Description = db.Column(db.String(255))
    status = db.Column(db.Enum('Paid', 'Unpaid', 'Pending'), nullable=False, default='Unpaid')
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Reminder(db.Model):
    __tablename__ = 'reminders'
    ReminderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('Users.UserId'))
    BillId = db.Column(db.Integer, db.ForeignKey('BillPayments.BillId'))
    reminder_date = db.Column(db.Date, nullable=False)
    message = db.Column(db.String(255), nullable=False)
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Goal(db.Model):
    __tablename__ = 'goals'
    GoalId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('Users.UserId'))
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Numeric(10, 2), nullable=False)
    saved_amount = db.Column(db.Numeric(10, 2), default=0)
    target_date = db.Column(db.Date, nullable=False)
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Budget(db.Model):
    __tablename__ = 'budgets'
    BudgetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    CategoryId = db.Column(db.Integer, db.ForeignKey('Categories.CategoryId'))
    budget_amount = db.Column(db.Numeric(10, 2), nullable=False)
    TransactionId = db.Column(db.Integer, db.ForeignKey('Transactions.TransactionId'))
    Amount = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String(255))
    creation_date = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    status = db.Column(db.Enum('Active', 'Inactive'), nullable=False, default='Active')
    amount_pending = db.Column(db.Numeric(10, 2), default=0)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Receipt(db.Model):
    __tablename__ = 'receipts'
    ReceiptId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TransactionId = db.Column(db.Integer, db.ForeignKey('Transactions.TransactionId'))
    UserId = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    ReceiptDate = db.Column(db.Date, nullable=False)
    Description = db.Column(db.String(255))
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    NotificationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    CreatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    UpdatedAt = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
