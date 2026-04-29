from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Зарегистрироваться')

class ReviewForm(FlaskForm):
    rating = IntegerField('Оценка (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    text = TextAreaField('Отзыв', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Опубликовать')

class EditProfileForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')