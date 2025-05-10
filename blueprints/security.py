from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from models import User, Employee
from sqlalchemy import func, text
import os
import platform
import psutil
import datetime

security_bp = Blueprint('security', __name__, url_prefix='/security')

@security_bp.before_request
@login_required
def check_security_access():
    # Check if the user has access to security module
    if not current_user.has_security_access():
        flash('Você não tem permissão para acessar o módulo de segurança.', 'danger')
        return redirect(url_for('dashboard.index'))

@security_bp.route('/')
def index():
    # Get system information
    system_info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'python_version': platform.python_version(),
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent,
        'memory_available': round(psutil.virtual_memory().available / (1024 * 1024 * 1024), 2),  # in GB
        'memory_total': round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2),  # in GB
        'disk_usage': psutil.disk_usage('/').percent,
        'disk_available': round(psutil.disk_usage('/').free / (1024 * 1024 * 1024), 2),  # in GB
        'disk_total': round(psutil.disk_usage('/').total / (1024 * 1024 * 1024), 2),  # in GB
        'server_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Get application statistics
    app_stats = {
        'user_count': User.query.count(),
        'employee_count': Employee.query.count(),
        'admin_count': User.query.filter_by(role='admin').count(),
        'management_count': User.query.filter_by(role='management').count(),
        'employee_user_count': User.query.filter_by(role='employee').count()
    }
    
    # Get database statistics
    db_stats = {}
    try:
        # Number of tables
        result = db.session.execute(text("SELECT COUNT(*) FROM sqlite_master WHERE type='table'"))
        db_stats['table_count'] = result.scalar()
        
        # Database size
        db_path = os.environ.get("DATABASE_URL", "sqlite:///unbug.db").replace("sqlite:///", "")
        if os.path.exists(db_path):
            db_stats['db_size'] = round(os.path.getsize(db_path) / (1024 * 1024), 2)  # in MB
        else:
            db_stats['db_size'] = 'N/A'
        
        # Table counts
        tables = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
        table_rows = {}
        for table in tables:
            count = db.session.execute(text(f"SELECT COUNT(*) FROM {table[0]}")).scalar()
            table_rows[table[0]] = count
        db_stats['table_rows'] = table_rows
        
    except Exception as e:
        db_stats['error'] = str(e)
    
    # Get recent logins (would need to add a login tracking table for this)
    # This is a placeholder
    recent_logins = []
    
    # Get recent activity (would need to add an activity tracking table for this)
    # This is a placeholder
    recent_activity = []
    
    return render_template('security/index.html',
                           system_info=system_info,
                           app_stats=app_stats,
                           db_stats=db_stats,
                           recent_logins=recent_logins,
                           recent_activity=recent_activity)
