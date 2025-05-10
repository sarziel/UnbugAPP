from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from models import User
from forms import LoginForm, ChangePasswordForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            
            # Check if there's a 'next' parameter in the request, redirecting to that page if it exists
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for('dashboard.index'))
        
        flash('Usuário ou senha inválidos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.current_password.data):
            # Set the new password
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            
            flash('Senha alterada com sucesso!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Senha atual incorreta.', 'danger')
    
    return render_template('auth/change_password.html', form=form)
