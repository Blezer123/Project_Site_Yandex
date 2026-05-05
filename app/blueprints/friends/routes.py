from flask import Blueprint, render_template
from flask_login import login_required

friends_bp = Blueprint('friends', __name__, url_prefix='/friends')


@friends_bp.route('/requests')
@login_required
def requests():
    return render_template('friends/requests.html')


@friends_bp.route('/add/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    return '<h1>Заявка отправлена (заглушка)</h1><a href="/">На главную</a>'


@friends_bp.route('/accept/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    return '<h1>Заявка принята (заглушка)</h1><a href="/">На главную</a>'


@friends_bp.route('/reject/<int:request_id>', methods=['POST'])
@login_required
def reject_request(request_id):
    return '<h1>Заявка отклонена (заглушка)</h1><a href="/">На главную</a>'


@friends_bp.route('/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    return '<h1>Друг удалён (заглушка)</h1><a href="/">На главную</a>'


def get_friends(user_id):
    """Заглушка - возвращает пустой список друзей"""
    return []