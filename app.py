import os
import logging
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize SQLAlchemy with declarative base
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Initialize Flask-Login
login_manager = LoginManager()

def create_app():
    # Create Flask app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///unbug.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'
    
    with app.app_context():
        # Import models
        from models import User, Employee, Client, Supplier, ServiceOrder, Project, InventoryItem, FinancialEntry
        
        # Create database tables
        db.create_all()
        
        # Create admin user if not exists
        from werkzeug.security import generate_password_hash
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                email='admin@unbug.com'
            )
            db.session.add(admin)
            
            # Add predefined users
            users = [
                User(username='ceounbug', password_hash=generate_password_hash('unbug123'), 
                     role='management', email='ceo@unbug.com'),
                User(username='operacoesunbug', password_hash=generate_password_hash('unbug123'), 
                     role='management', email='operations@unbug.com'),
                User(username='rhunbug', password_hash=generate_password_hash('unbug123'), 
                     role='management', email='hr@unbug.com')
            ]
            db.session.add_all(users)
            db.session.commit()
        
        # Register blueprints
        from blueprints.auth import auth_bp
        from blueprints.dashboard import dashboard_bp
        from blueprints.orders import orders_bp
        from blueprints.finance import finance_bp
        from blueprints.inventory import inventory_bp
        from blueprints.employees import employees_bp
        from blueprints.clients import clients_bp
        from blueprints.security import security_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(orders_bp)
        app.register_blueprint(finance_bp)
        app.register_blueprint(inventory_bp)
        app.register_blueprint(employees_bp)
        app.register_blueprint(clients_bp)
        app.register_blueprint(security_bp)
        
        # Root route
        @app.route('/')
        def index():
            if current_user.is_authenticated:
                return redirect(url_for('dashboard.index'))
            return redirect(url_for('auth.login'))
            
        @login_manager.user_loader
        def load_user(user_id):
            from models import User
            return User.query.get(int(user_id))
            
        return app

app = create_app()
