"""
Sentilytics — Admin Routes
Admin-only routes for system management and overview.
"""

from flask import Blueprint, render_template
from flask_login import login_required

from app.auth.decorators import admin_required
from app.services.user_service import get_all_users, get_total_users, get_total_admins
from app.services.prediction_service import get_all_metrics
from app.services.dataset_service import get_model_status, get_dataset_files

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Admin panel with system overview."""
    users = get_all_users()
    total_users = get_total_users()
    total_admins = get_total_admins()
    model_status = get_model_status()
    all_metrics = get_all_metrics()
    dataset_files = get_dataset_files()

    # Count trained models
    models_trained = sum(1 for m in model_status if m['model_exists'])

    # Count available datasets
    datasets_count = sum(1 for f in dataset_files if f['exists'])

    return render_template('admin_dashboard.html',
                           users=users,
                           total_users=total_users,
                           total_admins=total_admins,
                           model_status=model_status,
                           models_trained=models_trained,
                           datasets_count=datasets_count,
                           all_metrics=all_metrics)
