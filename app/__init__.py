from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

from app.extensions import db
from app.models import User

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Настройки

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gamehub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/avatars'
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

    # База данных

    db.init_app(app)

    # Авторизация
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Регистрируем blueprints

    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.main.routes import main_bp
    from app.blueprints.profile.routes import profile_bp
    from app.blueprints.games.routes import games_bp
    from app.blueprints.friends.routes import friends_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(games_bp, url_prefix='/games')
    app.register_blueprint(friends_bp, url_prefix='/friends')

    # Создаём таблицы

    with app.app_context():
        db.create_all()

    return app