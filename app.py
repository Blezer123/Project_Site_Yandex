from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
# Используем надёжный секретный ключ
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Проверяем, заполнены ли все поля
        if not username or not email or not password or not confirm_password:
            flash('Все поля должны быть заполнены!', 'error')
        # Проверяем совпадение паролей
        elif password != confirm_password:
            flash('Пароли не совпадают!', 'error')
        # Проверяем минимальную длину пароля
        elif len(password) < 6:
            flash('Пароль должен содержать минимум 6 символов!', 'error')
        else:
            # Если все проверки пройдены — показываем сообщение об успехе
            flash(f'Регистрация успешна! Пользователь {username} создан.', 'success')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/')
def index():
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)