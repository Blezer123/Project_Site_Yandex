from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Review, Friend
from werkzeug.security import generate_password_hash, check_password_hash

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/<int:user_id>')
@login_required
def view(user_id):
    user = User.query.get_or_404(user_id)

    # Получаем отзывы пользователя

    reviews = Review.query.filter_by(user_id=user_id).all()

    # Получаем список друзей

    friends = []
    sent = Friend.query.filter_by(from_user_id=user_id, status='accepted').all()
    received = Friend.query.filter_by(to_user_id=user_id, status='accepted').all()
    for f in sent:
        friends.append(f.to_user)
    for f in received:
        friends.append(f.from_user)

    return render_template('profile/view.html', user=user, reviews=reviews, friends=friends)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        # Проверяем имя

        if username and username != current_user.username:
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash('Пользователь с таким именем уже существует', 'error')
            else:
                current_user.username = username
                flash('Имя обновлено', 'success')

        # Проверяем email

        if email and email != current_user.email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                flash('Пользователь с такой почтой уже существует', 'error')
            else:
                current_user.email = email
                flash('Email обновлён', 'success')

        # Меняем пароль

        if old_password and new_password:
            if check_password_hash(current_user.password, old_password):
                if len(new_password) >= 6:
                    current_user.password = generate_password_hash(new_password)
                    flash('Пароль изменён', 'success')
                else:
                    flash('Новый пароль должен быть не менее 6 символов', 'error')
            else:
                flash('Старый пароль введён неверно', 'error')

        db.session.commit()
        return redirect(url_for('profile.view', user_id=current_user.id))

    return render_template('profile/edit.html', user=current_user)


@profile_bp.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash('Нельзя удалить чужой отзыв', 'error')
        return redirect(url_for('profile.view', user_id=current_user.id))

    db.session.delete(review)
    db.session.commit()
    flash('Отзыв удалён', 'success')
    return redirect(url_for('profile.view', user_id=current_user.id))