import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    # MySQL configurations
    MYSQL_HOST = '100.122.226.52'
    MYSQL_USER = 'Anwesa'
    MYSQL_PASSWORD = 'A123'
    MYSQL_DB = 'wealthapp'
    # SQLAlchemy configurations
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://Anwesa:A123@100.122.226.52/wealthapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT configurations
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_secret_key'
