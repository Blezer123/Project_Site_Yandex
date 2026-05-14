import requests
import os
from datetime import datetime


class IGDBService:
    def __init__(self):
        self.client_id = os.getenv('IGDB_CLIENT_ID')
        self.access_token = os.getenv('IGDB_ACCESS_TOKEN')
        self.url = 'https://api.igdb.com/v4/games'

    def search_games(self, query):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'text/plain'
        }
        data = f'search "{query}"; fields name, cover.image_id, first_release_date, rating; limit 20;'

        response = requests.post(self.url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        return []

    def format_game(self, game):
        cover_id = game.get('cover', {}).get('image_id') if game.get('cover') else None

        # Преобразуем дату

        release_date = game.get('first_release_date')
        year = ''
        if release_date:
            try:
                year = datetime.fromtimestamp(release_date).strftime('%Y')
            except:
                year = ''

        # Преобразуем рейтинг

        rating_100 = game.get('rating', 0)

        return {
            'id': game.get('id'),
            'title': game.get('name', 'Без названия'),
            'cover': f"https://images.igdb.com/igdb/image/upload/t_cover_big/{cover_id}.jpg" if cover_id else None,
            'year': year,
            'rating': round(rating_100 / 20, 1) if rating_100 else None
        }