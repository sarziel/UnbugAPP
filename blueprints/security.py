from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import User, Employee
from sqlalchemy import func, text
from werkzeug.security import generate_password_hash
import os
import platform
import psutil
import datetime
import forms

security_bp = Blueprint('security', __name__, url_prefix='/security')

@security_bp.before_request
@login_required
def check_security_access():
    if request.endpoint != 'security.app_info':  # Allow public access to app_info
        # Check if the user has access to security module
        if not current_user.has_security_access():
            flash('Você não tem permissão para acessar o módulo de segurança.', 'danger')
            return redirect(url_for('dashboard.index'))

@security_bp.route('/')
def index():
    # Get system information
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    uptime_str = f"{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds // 60) % 60}m"
    
    system_info = {
        'os': f"{platform.system()} {platform.version()}",
        'python_version': platform.python_version(),
        'ip': request.host,
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'uptime': uptime_str,
        'database': 'PostgreSQL',
        'last_updated': datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    
    # Get users for system users table
    users = User.query.all()
    
    # Mock login logs (would need a real table for this in production)
    login_logs = [
        {
            'username': 'admin',
            'activity': 'Login bem-sucedido',
            'ip_address': '192.168.1.100',
            'timestamp': datetime.datetime.now() - datetime.timedelta(minutes=15)
        },
        {
            'username': 'maria.silva',
            'activity': 'Login bem-sucedido',
            'ip_address': '192.168.1.101',
            'timestamp': datetime.datetime.now() - datetime.timedelta(hours=2)
        },
        {
            'username': 'carlos.ferreira',
            'activity': 'Tentativa de login malsucedida',
            'ip_address': '192.168.1.102',
            'timestamp': datetime.datetime.now() - datetime.timedelta(hours=3)
        }
    ]
    
    return render_template('security/index.html',
                           system_info=system_info,
                           users=users,
                           login_logs=login_logs)


@security_bp.route('/users')
def users():
    """Página de gerenciamento de usuários"""
    users = User.query.all()
    return render_template('security/users.html', users=users)


@security_bp.route('/user/new', methods=['GET', 'POST'])
def new_user():
    """Criar novo usuário"""
    form = forms.UserForm()
    
    if form.validate_on_submit():
        # Criar novo usuário
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.role = form.role.data
        user._is_active = form.active.data
        
        # Criar funcionário associado
        employee = Employee()
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.position = form.position.data
        employee.department = form.department.data
        employee.phone = form.phone.data
        employee.hire_date = form.hire_date.data
        employee.active = form.active.data
        
        # Associar usuário e funcionário
        employee.user = user
        
        db.session.add(user)
        db.session.add(employee)
        db.session.commit()
        
        flash(f'Usuário "{user.username}" criado com sucesso.', 'success')
        return redirect(url_for('security.users'))
    
    return render_template('security/user_form.html', form=form, title="Novo Usuário")


@security_bp.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    """Editar usuário existente"""
    user = User.query.get_or_404(id)
    employee = user.employee
    
    if not employee:
        flash('Usuário não possui perfil de funcionário associado.', 'danger')
        return redirect(url_for('security.users'))
    
    form = forms.UserForm(original_username=user.username)
    
    # Pré-preencher o formulário na requisição GET
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role.data = user.role
        form.active.data = user._is_active
        
        form.first_name.data = employee.first_name
        form.last_name.data = employee.last_name
        form.position.data = employee.position
        form.department.data = employee.department
        form.phone.data = employee.phone
        form.hire_date.data = employee.hire_date
    
    if form.validate_on_submit():
        # Atualizar usuário
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user._is_active = form.active.data
        
        # Se uma nova senha foi fornecida, atualizar
        if form.password.data:
            user.set_password(form.password.data)
        
        # Atualizar funcionário
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.position = form.position.data
        employee.department = form.department.data
        employee.phone = form.phone.data
        employee.hire_date = form.hire_date.data
        employee.active = form.active.data
        
        db.session.commit()
        
        flash(f'Usuário "{user.username}" atualizado com sucesso.', 'success')
        return redirect(url_for('security.users'))
    
    return render_template('security/user_form.html', form=form, user=user, title="Editar Usuário")


@security_bp.route('/user/toggle/<int:id>', methods=['POST'])
def toggle_user(id):
    """Ativa/desativa um usuário"""
    user = User.query.get_or_404(id)
    
    if user.username == 'admin':
        flash('Não é possível desativar o usuário administrador principal.', 'danger')
    else:
        user._is_active = not user._is_active
        status = 'ativado' if user._is_active else 'desativado'
        db.session.commit()
        flash(f'Usuário "{user.username}" {status} com sucesso.', 'success')
    
    return redirect(url_for('security.users'))


@security_bp.route('/user/reset_password/<int:id>', methods=['POST'])
def reset_password(id):
    """Resetar senha de um usuário para a senha padrão"""
    user = User.query.get_or_404(id)
    
    # Define a senha padrão como "mudar123"
    user.set_password('mudar123')
    db.session.commit()
    
    flash(f'Senha do usuário "{user.username}" foi resetada. Nova senha: mudar123', 'success')
    return redirect(url_for('security.users'))


@security_bp.route('/config')
def config():
    """Configurações do sistema"""
    return render_template('security/config.html')

@security_bp.route('/reset_admin', methods=['POST'])
def reset_admin():
    """Recria o usuário admin"""
    from werkzeug.security import generate_password_hash
    
    # Verifica se já existe um admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@unbug.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            _is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        flash('Usuário admin recriado com sucesso! Senha: admin123', 'success')
    else:
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        flash('Senha do admin resetada! Nova senha: admin123', 'success')
    
    return redirect(url_for('security.users'))


@security_bp.route('/app_info')
def app_info():
    """Retorna informações do app em formato JSON"""
    info = {
        'name': 'Unbug Solutions TI - ERP',
        'version': '1.0.0',
        'database': 'PostgreSQL',
        'server_time': datetime.datetime.now().isoformat(),
        'users_count': User.query.count(),
        'employees_count': Employee.query.count()
    }
    return jsonify(info)
