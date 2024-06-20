# app/__init__.py

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)

# Load configuration from config.py
app.config.from_object('app.config.Config')

mysql = MySQL(app)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if user is not authenticated

from app import routes  # Import routes after initializing the app
