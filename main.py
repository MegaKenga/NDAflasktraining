import os
import sqlite3

from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g

from FDataBase import FDataBase

DATABASE = '/flsite.db'
DEBUG = True
SECRET_KEY = 'v3dfs15d6fsgtrh4tyjn5tba65sf4fc6a14gfv4e8r4ghebd'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd5fg4s65dfg456g1vg2ads1v56ds45646'
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE']) #создаем соединение
    conn.row_factory = sqlite3.Row # записи из БД будут не в виде кортежа, а в виде словаря
    return conn # возвращает соединение с БД


def get_db(): #создание соединения, если оно еще не установлено
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def create_db(): #Функция для создания таблиц БД
    db = connect_db() # Вызываем функцию
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


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

@app.route('/registration')
def registration_page():
    return render_template('registration.html', title='Регистрация')


@app.route('/brands')
def brands_page():
    return render_template('brands.html', brands=dbase.getBrands(), title='Каталог по производителям')


@app.route('/units')
def units_page():
    return render_template('units.html', units=dbase.getBusinessUnits(), title='Каталог по направлениям')


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
    return render_template('news.html', news=dbase.getNewsAnonce(), title='Новости')

@app.route('/news/<int:id_news>')
def showNews(id_news):
    title, text = dbase.getNews(id_news)
    if not title:
        abort(404)
    return render_template('post.html', title=title, text=text)

@app.route('/add_news', methods=["POST", "GET"])
def add_news_page():
    if request.method == "POST":
        result = dbase.addNews(request.form['name'], request.form['post'])
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
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена'), 404 #для отображения ошибки в серверной части

@app.route('/brands/<brand>')
def brand(brand):
    return render_template(f'{brand}.html', brand=brand, title ='{{brand}}')