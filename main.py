from flask import Flask, render_template, url_for, request, flash, redirect, abort, g, make_response
from FDataBase import FDataBase
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
from admin.admin import admin
import sqlite3
import os

DATABASE = 'tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'sdfg54sd56fg4sdf2g1sd65gf46sd4g56sdfg'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.register_blueprint(admin, url_prefix='/admin')

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
    return render_template('index.html', brands=dbase.get_brands(), units=dbase.get_business_units(), title='НДА Деловая медицинская компания')


@app.route('/secret')
@login_required
def secret_page():
    return render_template('secret.html', title='Ну очень секретная страница')


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(request.form['psw'])
        res = dbase.addUser(form.name.data, form.email.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")

    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/profile')
@login_required
def profile_page():
    return render_template('profile.html', title='Профиль')


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                    return redirect(url_for('profile'))
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")

    return redirect(url_for('profile_page'))

@app.route('/authorisation', methods=['POST', 'GET'])
def authorisation_page():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            user_auth = UserLogin().create_user(user)
            rm = form.remember.data
            login_user(user_auth, remember=rm)
            return redirect(request.args.get('next') or url_for('profile_page'))
        else:
            flash('Неправильно указано имя или пароль', 'error')
    return render_template("authorisation.html", title="Авторизация", form=form)

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


@app.route('/<brand>')
def brand_page(brand):
    brand = dbase.get_single_brand(brand)
    return render_template('brand_page.html', brand=brand, title=brand)

@app.route('/brandimage')
def brand_image(brand):
    img = dbase.get_brand_image(brand)
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route("/brands/<alias>")
@login_required
def showBrands(alias):
    name, url = dbase.getPost(alias)
    if not name:
        abort(404)