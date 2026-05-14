from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Friend

friends_bp = Blueprint('friends', __name__, url_prefix='/friends')


# Страница с заявками

@friends_bp.route('/requests')
@login_required
def requests_list():
    # Заявки которые отправили мне

    incoming = Friend.query.filter_by(to_user_id=current_user.id, status='pending').all()
    # Заявки которые я отправил

    outgoing = Friend.query.filter_by(from_user_id=current_user.id, status='pending').all()

    return render_template('friends/requests.html', incoming=incoming, outgoing=outgoing)


# Отправить заявку
@friends_bp.route('/add/<int:user_id>', methods=['POST'])
@login_required
def send_request(user_id):
    to_user = User.query.get_or_404(user_id)

    # Нельзя добавить самого себя

    if to_user.id == current_user.id:
        flash('Нельзя добавить самого себя в друзья!', 'error')
        return redirect(url_for('profile.view', user_id=user_id))

    # Проверяем есть ли уже заявка

    existing = Friend.query.filter(
        ((Friend.from_user_id == current_user.id) & (Friend.to_user_id == to_user.id)) |
        ((Friend.from_user_id == to_user.id) & (Friend.to_user_id == current_user.id))
    ).first()

    if existing:
        if existing.status == 'accepted':
            flash('Вы уже друзья!', 'warning')
        elif existing.status == 'pending':
            if existing.from_user_id == current_user.id:
                flash('Вы уже отправили заявку этому пользователю!', 'warning')
            else:
                flash('Пользователь уже отправил вам заявку!', 'warning')
        return redirect(url_for('profile.view', user_id=user_id))

    # Создаём новую заявку

    new_request = Friend(
        from_user_id=current_user.id,
        to_user_id=to_user.id,
        status='pending'
    )
    db.session.add(new_request)
    db.session.commit()

    flash(f'Заявка в друзья отправлена пользователю {to_user.username}!', 'success')
    return redirect(url_for('profile.view', user_id=user_id))


# Принять заявку
@friends_bp.route('/accept/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    friend_request = Friend.query.get_or_404(request_id)

    if friend_request.to_user_id != current_user.id:
        flash('Это не ваша заявка!', 'error')
        return redirect(url_for('friends.requests_list'))

    if friend_request.status != 'pending':
        flash('Эта заявка уже обработана!', 'warning')
        return redirect(url_for('friends.requests_list'))

    friend_request.status = 'accepted'
    db.session.commit()

    flash(f'Вы теперь друзья с {friend_request.from_user.username}!', 'success')
    return redirect(url_for('friends.requests_list'))


# Отклонить заявку в друзья
@friends_bp.route('/reject/<int:request_id>', methods=['POST'])
@login_required
def reject_request(request_id):
    friend_request = Friend.query.get_or_404(request_id)

    if friend_request.to_user_id != current_user.id:
        flash('Это не ваша заявка!', 'error')
        return redirect(url_for('friends.requests_list'))

    db.session.delete(friend_request)
    db.session.commit()

    flash(f'Заявка от {friend_request.from_user.username} отклонена', 'info')
    return redirect(url_for('friends.requests_list'))


# Удаление из друзей

@friends_bp.route('/remove/<int:user_id>', methods=['POST'])
@login_required
def remove_friend(user_id):
    friendship = Friend.query.filter(
        ((Friend.from_user_id == current_user.id) & (Friend.to_user_id == user_id)) |
        ((Friend.from_user_id == user_id) & (Friend.to_user_id == current_user.id)),
        Friend.status == 'accepted'
    ).first()

    if not friendship:
        flash('Этот пользователь не в ваших друзьях!', 'warning')
        return redirect(url_for('profile.view', user_id=user_id))

    db.session.delete(friendship)
    db.session.commit()

    flash('Пользователь удалён из друзей', 'info')
    return redirect(url_for('profile.view', user_id=user_id))

# Поиск друзей

@friends_bp.route('/add_by_name', methods=['GET', 'POST'])
@login_required
def add_by_name():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()

        if not username:
            flash('Введите имя пользователя', 'error')
            return redirect(url_for('friends.add_by_name'))

        # Ищем пользователя

        user = User.query.filter_by(username=username).first()

        if not user:
            flash(f'Пользователь "{username}" не найден', 'error')
            return redirect(url_for('friends.add_by_name'))

        if user.id == current_user.id:
            flash('Нельзя добавить самого себя', 'error')
            return redirect(url_for('friends.add_by_name'))

        # Проверяем есть ли уже заявка

        existing = Friend.query.filter(
            ((Friend.from_user_id == current_user.id) & (Friend.to_user_id == user.id)) |
            ((Friend.from_user_id == user.id) & (Friend.to_user_id == current_user.id))
        ).first()

        if existing:
            if existing.status == 'accepted':
                flash('Вы уже друзья', 'warning')
            else:
                flash('Заявка уже отправлена', 'warning')
            return redirect(url_for('friends.add_by_name'))

        # Отправляем заявку

        new_request = Friend(
            from_user_id=current_user.id,
            to_user_id=user.id,
            status='pending'
        )
        db.session.add(new_request)
        db.session.commit()

        flash(f'Заявка отправлена пользователю {user.username}!', 'success')
        return redirect(url_for('friends.add_by_name'))

    return render_template('friends/add_by_name.html')