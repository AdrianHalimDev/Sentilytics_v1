"""
Sentilytics — Authentication Routes
Handles login, register, and logout functionality.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models_db import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email dan password harus diisi.', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.is_active:
                flash('Akun Anda telah dinonaktifkan.', 'danger')
                return render_template('login.html')

            login_user(user)
            flash(f'Selamat datang, {user.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard'))
        else:
            flash('Email atau password salah.', 'danger')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        errors = []
        if not name:
            errors.append('Nama harus diisi.')
        if not email:
            errors.append('Email harus diisi.')
        if not password:
            errors.append('Password harus diisi.')
        if len(password) < 6:
            errors.append('Password minimal 6 karakter.')
        if password != confirm_password:
            errors.append('Konfirmasi password tidak cocok.')

        # Check duplicate email
        if User.query.filter_by(email=email).first():
            errors.append('Email sudah terdaftar.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('register.html', name=name, email=email)

        # Create new user
        user = User(name=name, email=email, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('Anda telah logout.', 'info')
    return redirect(url_for('auth.login'))
