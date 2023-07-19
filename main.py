from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from flsite import get_db
from FDataBase import FDataBase
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd5fg4s65dfg456g1vg2ads1v56ds45646'
app.config.from_object(__name__)
login_manager = LoginManager(app)

dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error): #Закрываем соединение, если оно было установлено
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


# @app.route('/authorisation', methods=['POST', 'GET'])
# def authorisation_page():
    # if 'userLogged' in session:
    #     return redirect(url_for('profile', username=session['userLogged']))
    # elif request.method == 'POST' and request.form['username'] == 'teamNDA' and request.form['psw'] == 'NDA7140614':
    #     session['userLogged'] = request.form['username']
    #     return redirect(url_for('profile', username=session['userLogged']))
    # return render_template('authorisation.html', title='Авторизация')


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


@app.route('/authorisation', methods=['POST', 'GET'])
def authorisation_page():
    if request.method == 'POST':
        user = dbase.get_user_by_email(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            user_auth = UserLogin().create_user(user)
            login_user(user_auth)
            flash('Авторизация прошла успешно', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неправильно указано имя или пароль', 'error')

    return render_template('authorisation.html', title='Авторизация')


app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('authorisation_page'))


app.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for ('logout')}">Выйти из профиля</a>
    <p>user info: {current_user.get_id()}"""


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


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'Пользователь {username}'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена'), 404 #для отображения ошибки в серверной части


@app.route('/brands')
def brands_page():
    return render_template('brands.html', brands=dbase.get_brands(), title='Каталог по производителям')


@app.route('/units')
def units_page():
    return render_template('units.html', units=dbase.get_business_units(), title='Каталог по направлениям')
@app.route('/brands/<medicalbrand>')
def brand(medicalbrand):
    return render_template(f'{medicalbrand}.html', medicalbrand=brand, title ='{{brand}}')
