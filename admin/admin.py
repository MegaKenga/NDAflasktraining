from flask import Blueprint, request, redirect, url_for, render_template, flash, session, g
import sqlite3


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

db = None


@admin.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    # Закрываем соединение, если оно было установлено
    global db
    db = None
    return request


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.logout', 'title': 'Выйти'}]


def login_admin():
    session['admin_logged'] = 1


def is_logged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not is_logged():
        return redirect(url_for('.login_page'))
    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=['POST', 'GET'])
def login_page():
    if is_logged():
        return redirect(url_for('.index'))
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Неверная пара логин/пароль', 'error')
    return render_template('admin/login.html', title='Панель администратора')


@admin.route('logout')
def logout():
    if not is_logged():
        return redirect(url_for('.login_page'))
    logout_admin()
    return redirect(url_for('.login_page'))


@admin.route('/list-brands')
def list_brands():
    if not is_logged():
        return redirect(url_for('.login_page'))
    brandlist = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, url FROM brands")
            brandlist = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД " + str(e))

    return render_template('admin/list-brands.html', title='Список брендов', menu=menu, list=brandlist)
