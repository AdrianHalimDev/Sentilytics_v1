"""
Sentilytics — User Service
Provides user-related queries for admin panel.
"""

from app.models_db import User


def get_all_users():
    """Get all users ordered by creation date."""
    return User.query.order_by(User.created_at.desc()).all()


def get_total_users():
    """Get total number of users."""
    return User.query.count()


def get_total_admins():
    """Get total number of admin users."""
    return User.query.filter_by(role='admin').count()
