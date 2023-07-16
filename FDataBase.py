import math
import time
import sqlite3


class FDataBase():
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getBrands(self):
        sql = """SELECT * FROM brands"""
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result: return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getBrands вернет пустой список

    def getBusinessUnits(self):
        sql = """SELECT * FROM business_units"""
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result: return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getBrands вернет пустой список

    def getGroups(self):
        sql = """SELECT * FROM groups"""
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
            if result: return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getGroups вернет пустой список

    def addNews(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO news VALUES(NULL, ?, ?, ?)', (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as err:
            print('Ошибка добавления в базу данных' + str(err))
            return False
        return True

    def getNews(self, id_news):
        try:
            self.__cur.execute(f'SELECT title, text FROM news WHERE id = {id_news} LIMIT 1')
            result = self.__cur.fetchone()
            if result: return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getNews вернет пустой список

    def getNewsAnonce(self):
        try:
            self.__cur.execute('SELECT title, text, id FROM news ORDER BY time DESC')
            result = self.__cur.fetchall()
            if result: return result
        except:
            print('Ошибка чтения из БД')
        return [] #Если произошла ошибка, то метод getNews вернет пустой список