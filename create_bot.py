import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database.sqlite_db import DataBase
# from database.pg_db import DataBase
import os
import config

logging.basicConfig(level=logging.INFO)

db = DataBase('tg.db')
# db = DataBase()
storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
# bot = Bot(token=os.environ.get('API_TOKEN'))
dp = Dispatcher(bot, storage=storage)
