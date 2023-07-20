import math
import time
import sqlite3


class FDataBase():
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_brands(self):
        sql = """SELECT * FROM brands"""
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result:
                return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getBrands вернет пустой список

    def get_business_units(self):
        sql = """SELECT * FROM business_units"""
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result:
                return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getBrands вернет пустой список

    def get_groups(self):
        sql = """SELECT * FROM groups"""
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result:
                return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getGroups вернет пустой список

    def add_news(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO news VALUES(NULL, ?, ?, ?)', (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as err:
            print('Ошибка добавления в базу данных' + str(err))
            return False
        return True

    def get_news(self, id_news):
        try:
            self.__cur.execute(f"SELECT title, text FROM news WHERE id = '{id_news}' LIMIT 1")
            result = self.__cur.fetchone()
            if result:
                return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getNews вернет пустой список

    def get_news_anonce(self):
        try:
            self.__cur.execute('SELECT title, text, id FROM news ORDER BY time DESC')
            result = self.__cur.fetchall()
            if result:
                return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getNewsanonce вернет пустой список

    def add_user(self, username, email, hashed_psw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email like '{email}'")
            result = self.__cur.fetchone()
            if result ['count'] > 0:
                print('Пользователь с таким адресом электронной почты уже существует')
                return False
            else:
                tm = math.floor(time.time())
                self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?)", (username, email, hashed_psw, tm))
                self.__db.commit()
        except sqlite3.Error as err:
            print('Ошибка добавления в базу данных' + str(err))
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            result = self.__cur.fetchone()
            if not result:
                print('Пользователь не найден')
                return False
            else:
                return result

        except sqlite3.Error as err:
            print('Ошибка получения данных пользователя' + str(err))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            result = self.__cur.fetchone()
            if not result:
                print('Пользователь не найден')
                return False
            else:
                return result

        except sqlite3.Error as err:
            print('Ошибка получения данных пользователя' + str(err))

        return False


