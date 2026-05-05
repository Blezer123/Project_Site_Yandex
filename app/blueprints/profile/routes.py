from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
def index():
    return '<h1>Страница профиля</h1>'

@profile_bp.route('/<int:user_id>')
@login_required
def view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile/view.html', user=user)