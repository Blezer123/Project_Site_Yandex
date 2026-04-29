from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User, Review, Friend

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/')
def index():
    return '<h1>Страница профиля (скоро будет)</h1>'