from flask import Blueprint

auth_bp = Blueprint('auth_bp', __name__)
user_bp = Blueprint('user_bp', __name__)
test_bp = Blueprint('test_bp',__name__)
transactions_bp = Blueprint('transactions_bp',__name__)
bill_bp = Blueprint('bill_bp',__name__)
reminders_bp = Blueprint('reminders_bp',__name__)
goals_bp = Blueprint('goals_bp',__name__)
budget_bp = Blueprint('budget_bp',__name__)
notifications_bp = Blueprint('notifications_bp',__name__)
receipts_bp = Blueprint('receipts_bp',__name__)
ml_bp = Blueprint('ml_bp',__name__)

from . import auth, user,test,transactions,bill,reminders,goals,budget,notifications,receipts,ml
