from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from flsite import get_db
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd5fg4s65dfg456g1vg2ads1v56ds45646'
app.config.from_object(__name__)


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


@app.route('/')
def main_page():
    return render_template('index.html', title='НДА Деловая медицинская компания')


@app.route('/authorisation')
def authorisation_page():
    return render_template('authorisation.html', title='Авторизация')


@app.route('/registration', methods = ['POST', 'GET'])
def registration_page():
    if request.method == 'POST':
        if len(request.form['username']) > 4 and len(request.form['email']) > 4 and len(request.form['psw']) > 4 and \
                request.form['psw'] == request.form['psw_repeat']:
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


@app.route('/brands')
def brands_page():
    return render_template('brands.html', brands=dbase.get_brands(), title='Каталог по производителям')


@app.route('/units')
def units_page():
    return render_template('units.html', units=dbase.get_business_units(), title='Каталог по направлениям')


@app.route('/contacts', methods=['POST', 'GET'])
def contacts_page():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки сообщения', category='error')
    print(url_for('contacts_page'))
    return render_template('contacts.html', title='Контакты')


@app.route('/login',  methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'teamNDA' and request.form['psw'] == 'NDA7140614':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация')


@app.route('/news')
def news_page():
    return render_template('news.html', news=dbase.get_news_anonce(), title='Новости')


@app.route('/news/<int:id_news>')
def showNews(id_news):
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


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f'Пользователь {username}'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена'), 404 #для отображения ошибки в серверной части


@app.route('/brands/<brand>')
def brand(brand):
    return render_template(f'{brand}.html', brand=brand, title ='{{brand}}')