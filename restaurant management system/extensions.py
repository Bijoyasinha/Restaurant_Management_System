from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-testing')

# Database configuration for MySQL with XAMPP
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://root:@localhost/restaurant_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# WTF CSRF configuration
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour

# Initialize database
db = SQLAlchemy(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Context processor to make csrf_token available in all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)
