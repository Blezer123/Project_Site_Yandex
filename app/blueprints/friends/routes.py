from flask import Blueprint

friends_bp = Blueprint('friends', __name__)

@friends_bp.route('/')
def index():
    return 'Друзья работают'