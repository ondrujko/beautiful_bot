import datetime
import sqlite3
# import schedule


async def is_old_booking(booking):
    now = datetime.datetime.now()
    day, month, year = int(booking[0]), int(booking[1]), int(booking[2])
    if year < now.year:
        return True
    if month < now.month:
        return True
    if day < now.day:
        return True
    return False


class DataBase:
    def __init__(self, db_path: str):
        """
        Подключиться к базе данных и создать таблицы

        :param db_path: нужен для подключения к базе данных
        """
        self.base = sqlite3.connect(db_path)
        self.cur = self.base.cursor()
        if self.base:
            print('Database connected OK!')
        self.base.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY)')
        self.base.execute('CREATE TABLE IF NOT EXISTS orders(day, month, year, time, id, status, contact, fio)')
        self.base.commit()

    async def add_new_user(self, chat_id: int):
        """
        Добавляет нового пользователя в базу данных.

        :param chat_id: нужен для добавления пользователя
        """
        self.cur.execute('INSERT OR IGNORE INTO users(id) VALUES(?)', (chat_id,))
        self.base.commit()

    async def add_new_order(self, day: int, month: int, year: int, time: str, chat_id: int, status: bool, contact: str,
                            fio: str):
        """
        Добавить новую бронь в базу данных
        """
        self.cur.execute(
            'INSERT OR IGNORE INTO orders(day, month, year, time, id, status, contact, fio) '
            'VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
            (day, month, year, time, chat_id, status, contact, fio,))
        self.base.commit()

    async def is_booking(self, day: int, month: int, year: int, time: str):
        """Узнать забронировано ли это окно.

        Принимает день, месяц, год, время.
        Возвращает булево значение
        True - забронировано
        False - свободно
        """
        result = self.cur.execute('SELECT * FROM orders WHERE day=? AND month=? AND year=? AND status=? AND time=?',
                                  (day, month, year, False, time)).fetchone()
        if result is None:
            return False
        else:
            return True

    async def search_booking(self, chat_id: int):
        """Узнать есть ли записи у пользователя. Если есть, то достать.

        Принимает chat_id. Ищет в базе данных.
        Если находит, то возвращает данные об этой записи.
        Если не находит, то возвращает False.
        """

        result = self.cur.execute('SELECT * FROM orders WHERE id=?', (chat_id,)).fetchone()
        if result is None:
            return False
        if await is_old_booking(result):
            return False
        return result

    async def delete_booking(self, chat_id: int):
        """
        Удаляет активную запись.

        :param chat_id: Нужен для поиска в базе данных.
        """
        if await self.search_booking(chat_id) is not False:
            self.cur.execute('DELETE FROM orders WHERE id=?', (chat_id,))
            self.base.commit()

    async def get_orders(self):
        self.cur.execute('SELECT * FROM orders')
        return self.cur.fetchall()
