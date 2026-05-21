"""
Sentilytics — Flask Application Factory
Creates and configures the Flask application with:
- SQLAlchemy for auth database
- Flask-Login for session management
- Blueprint registration for modular routes
- Admin seed from .env variables
"""

import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from dotenv import load_dotenv

from app.models_db import db, User

# Load environment variables
load_dotenv()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # ============================================
    # Configuration
    # ============================================
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentilytics.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ============================================
    # Initialize Extensions
    # ============================================
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ============================================
    # Register Blueprints
    # ============================================
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)

    # ============================================
    # Error handlers
    # ============================================
    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template('403.html'), 403

    # ============================================
    # Root redirect
    # ============================================
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # ============================================
    # Create database tables and seed admin
    # ============================================
    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Create admin account from .env if it doesn't exist."""
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    if not admin_email or not admin_password:
        print("[WARNING] ADMIN_EMAIL or ADMIN_PASSWORD not set in .env. Skipping admin seed.")
        return

    existing_admin = User.query.filter_by(email=admin_email).first()
    if existing_admin:
        print(f"[INFO] Admin account already exists: {admin_email}")
        return

    admin = User(
        name='Administrator',
        email=admin_email,
        role='admin',
        is_active=True
    )
    admin.set_password(admin_password)
    db.session.add(admin)
    db.session.commit()
    print(f"[INFO] Admin account created: {admin_email}")
