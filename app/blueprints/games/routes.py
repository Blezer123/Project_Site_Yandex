from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from app.services.igdb_service import IGDBService

games_bp = Blueprint('games', __name__, url_prefix='/games')
igdb = IGDBService()


@games_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    games = []

    if query:
        results = igdb.search_games(query)
        games = []
        if results:
            for g in results:
                games.append(igdb.format_game(g))
        if not games:
            flash('Игры не найдены', 'warning')

    return render_template('games/search.html', games=games, query=query)