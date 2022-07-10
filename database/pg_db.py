import datetime
import psycopg2
import os


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
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = os.environ.get('DATABASE_URL')

        self.connection = psycopg2.connect(database_url)

        with self.connection.cursor() as cursor:
            cursor.execute('SELECT version();')
            print(cursor.fetchone())
        with self.connection.cursor() as cursor:
            print('Database connected OK!')
            cursor.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY)')
            cursor.execute('CREATE TABLE IF NOT EXISTS orders(day INTEGER, month INTEGER, year INTEGER, time TEXT, '
                           'id INTEGER, status INTEGER, contact TEXT, fio TEXT)')
            self.connection.commit()

    async def add_new_user(self, chat_id: int):
        """
        Добавляет нового пользователя в базу данных.

        :param chat_id: нужен для добавления пользователя
        """

        with self.connection.cursor() as cur:
            cur.execute('INSERT INTO users(id) VALUES(%s) ON CONFLICT DO NOTHING', (chat_id,))
            self.connection.commit()

    async def add_new_order(self, day: int, month: int, year: int, time: str, chat_id: int, status: bool, contact: str,
                            fio: str):
        """
        Добавить новую бронь в базу данных
        """
        with self.connection.cursor() as cur:
            insert_query = """INSERT INTO orders(day, month, year, time, id, status, contact, fio) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
            cur.execute(insert_query, (day, month, year, time, chat_id, 1, contact, fio))
            self.connection.commit()

    async def is_booking(self, day: int, month: int, year: int, time: str):
        """Узнать забронировано ли это окно.

        Принимает день, месяц, год, время.
        Возвращает булево значение
        True - забронировано
        False - свободно
        """
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT * FROM orders WHERE day = ? AND month = ? AND year = ? AND time = ?"
                        f"VALUES (%s, %s, %s, %s)",
                        (day, month, year, time))
            result = cur.fetchone()
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
        with self.connection.cursor() as cur:

            cur.execute(f'SELECT * FROM orders WHERE id = %s', (chat_id,))
            result = cur.fetchone()
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
        with self.connection.cursor() as cur:
            if await self.search_booking(chat_id) is not False:
                cur.execute('DELETE FROM orders WHERE id=%s', (chat_id,))
                self.connection.commit()

    async def get_orders(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM orders')
            return cursor.fetchall()
