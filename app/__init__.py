from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Create Flask app
app = Flask(__name__)

# Configure your app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rxpress.db'  # Adjust as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1hatedatpass'

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes and models at the end to avoid circular imports
from app import routes
from app.models import User

from . import db
