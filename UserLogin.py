from flask_login import UserMixin


class UserLogin(UserMixin):
    def from_db(self, user_id, db):
        """Используется при создании объекта в декораторе UserLoader. Берет информацию о пользователе из БД
        возвращает экземпляр класса UsrLogin"""
        self.__user = db.get_user(user_id)
        return self

    def create_user(self, user):
        self.__user = user
        return self

    def get_id(self):
        """Функция возвращающая уникальный идентификатор пользователя(должен быть представлен в виде unicode строки)"""
        return str(self.__user['id'])

    """"Эти методы реализованы в UsrMixin"""
    # def is_authenticated(self):
    #     """Функция проверки аутентификации пользователя. True если авторизован, False если нет"""
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без email"

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), "rb") as f:
                    img = f.read()
            except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: " + str(e))
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == "png" or ext == "PNG":
            return True
        return False

