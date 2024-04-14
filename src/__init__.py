from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)

from src import spy, models

# Function to create admin role and user
def create_admin():
    with app.app_context():
        from src.models import Role, User
        # Create database tables if they don't exist
        db.create_all()

        # Check if the admin role exists, create it if not
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)

        # Check if the admin user exists, create it if not
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Hash the password
            admin_pwd = os.getenv('ADMIN_PASSWORD')
            print("admin_pwd: ", admin_pwd)
            hashed_password = bcrypt.generate_password_hash(admin_pwd).decode('utf-8')

            # Create the admin user
            admin_user = User(username='admin', password=hashed_password, role_id=admin_role.id)
            db.session.add(admin_user)

        # Commit changes to the database
        db.session.commit()

create_admin()