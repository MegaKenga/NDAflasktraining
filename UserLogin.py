class UserLogin():
    def from_db(self, user_id, db):
        """Используется при создании объекта в декораторе UserLoader. Берет информацию о пользователе из БД
        возвращает экземпляр класса UsrLogin"""
        self.__user = db.get_user(user_id)
        return self

    def create_user(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        """Функция проверки аутентификации пользователя. True если авторизован, False если нет"""
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        """Функция возвращающая уникальный идентификатор пользователя(должен быть представлен в виде unicode строки)"""
        return str(self.__user['id'])
