from flask import Flask, render_template, url_for, request, flash, redirect, abort, g
from FDataBase import FDataBase
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlite3
import os

DATABASE = 'tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'sdfg54sd56fg4sdf2g1sd65gf46sd4g56sdfg'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app)
login_manager.login_view = 'authorisation_page'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    # создание соединения, если оно еще не установлено
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()


@login_manager.user_loader
def load_user(user_id):
    print('Load User')
    return UserLogin().from_db(user_id, dbase)


@app.route('/')
def main_page():
    return render_template('index.html', title='НДА Деловая медицинская компания')


@app.route('/secret')
@login_required
def secret_page():
    return render_template('secret.html', title='Ну очень секретная страница')


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    if request.method == 'POST':
        if len(request.form['username']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 \
                and request.form['psw'] == request.form['psw_repeat']:
            hashed = generate_password_hash(request.form['psw'])
            result = dbase.add_user(request.form['username'], request.form['email'], hashed)
            if result:
                flash('Регистрация прошла успешно', 'success')
                return redirect(url_for('authorisation_page'))
            else:
                flash('Ошибка добавления в базу данных', 'error')
        else:
            flash('Неверно заполнены поля', 'error')

    return render_template('registration.html', title='Регистрация')


@app.route('/profile')
@login_required
def profile_page():
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
                    <p>user info: {current_user.get_id()}"""


@app.route('/authorisation', methods=['POST', 'GET'])
def authorisation_page():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page'))
    if request.method == 'POST':
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_auth = UserLogin().create_user(user)
            rm = True if request.form.get('rememberme') else False
            login_user(user_auth, remember=rm)
            return redirect(request.args.get('next') or url_for('profile_page'))
        else:
            flash('Неправильно указано имя или пароль', 'error')

    return render_template('authorisation.html', title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('authorisation_page'))


@app.route('/news')
def news_page():
    return render_template('news.html', news=dbase.get_news_anonce(), title='Новости')


@app.route('/news/<int:id_news>')
def show_news(id_news):
    text, title = dbase.get_news(id_news)
    if not title:
        abort(404)
    return render_template('post.html', text=text, title=title)


@app.route('/add_news', methods=["POST", "GET"])
def add_news_page():
    if request.method == "POST":
        result = dbase.add_news(request.form['name'], request.form['post'])
        if not result:
            flash('Ошибка добавления новости', category='error')
        else:
            flash('Успешно', category='success')
    return render_template('add_news.html', title='Добавить новость')


@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', title='Связаться с нами')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена'), 404
    # для отображения ошибки в серверной части


@app.route('/brands')
def brands_page():
    return render_template('brands.html', brands=dbase.get_brands(), title='Каталог по производителям')


@app.route('/units')
def units_page():
    return render_template('units.html', units=dbase.get_business_units(), title='Каталог по направлениям')


@app.route('/brands/<medicalbrand>')
def brand(medicalbrand):
    return render_template(f'{medicalbrand}.html', medicalbrand=brand, title={{brand}})
