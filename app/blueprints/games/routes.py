from flask import Blueprint

games_bp = Blueprint('games', __name__)

@games_bp.route('/search')
def search():
    return '<h1>Поиск игр (скоро будет)</h1>'