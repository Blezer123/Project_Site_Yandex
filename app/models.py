from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


# Таблица Пользователи

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(200), default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связи с другими таблицами
    reviews = db.relationship('Review', backref='author', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)
    sent_friend_requests = db.relationship('Friend', foreign_keys='Friend.from_user_id', backref='from_user', lazy=True)
    received_friend_requests = db.relationship('Friend', foreign_keys='Friend.to_user_id', backref='to_user', lazy=True)


# Таблица Игры

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, unique=True)  # ID из RAWG API
    title = db.Column(db.String(200), nullable=False)
    cover_url = db.Column(db.String(500))
    rawg_rating = db.Column(db.Float)
    released = db.Column(db.String(50))
    description = db.Column(db.Text)

    # Связи
    reviews = db.relationship('Review', backref='game', lazy=True)
    wishlist = db.relationship('Wishlist', backref='game', lazy=True)



# Таблица Рецензии

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-10
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Внешние ключи

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)


# Таблица Друзья

class Friend(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('from_user_id', 'to_user_id', name='unique_friendship'),)



# Таблица Вишлист

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'game_id', name='unique_wishlist'),)