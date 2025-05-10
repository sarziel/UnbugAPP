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
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'
    
    with app.app_context():
        # Import models
        from models import User, Employee, Client, Supplier, ServiceOrder, Project, InventoryItem, FinancialEntry
        
        # Create or update database tables
        with app.app_context():
            db.create_all()
            # Enable automatic table updates
            for table in db.metadata.tables.values():
                for column in table.columns:
                    column.nullable = True
            db.session.commit()
        
        # Create admin user if not exists
        from werkzeug.security import generate_password_hash
        from datetime import datetime
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                email='admin@unbug.com'
            )
            db.session.add(admin)
            db.session.flush()  # Para obter o ID do admin
            
            # Criar funcionário para o admin
            admin_employee = Employee(
                first_name='João',
                last_name='Silva',
                position='Gerente TI',
                department='TI',
                phone='(11) 91234-5678',
                hire_date=datetime.now().date(),
                active=True,
                user_id=admin.id
            )
            db.session.add(admin_employee)
            
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
            db.session.flush()  # Para obter IDs dos usuários
            
            # Criar funcionários para os demais usuários
            employees = [
                Employee(
                    first_name='Roberto',
                    last_name='Costa',
                    position='CEO',
                    department='Diretoria',
                    phone='(11) 99876-5432',
                    hire_date=datetime.now().date(),
                    active=True,
                    user_id=users[0].id
                ),
                Employee(
                    first_name='Carlos',
                    last_name='Oliveira',
                    position='Gerente de Operações',
                    department='Operações',
                    phone='(11) 98765-4321',
                    hire_date=datetime.now().date(),
                    active=True,
                    user_id=users[1].id
                ),
                Employee(
                    first_name='Ana',
                    last_name='Souza',
                    position='Gerente de RH',
                    department='Recursos Humanos',
                    phone='(11) 97654-3210',
                    hire_date=datetime.now().date(),
                    active=True,
                    user_id=users[2].id
                )
            ]
            db.session.add_all(employees)
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
