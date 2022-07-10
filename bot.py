from aiogram import executor
from create_bot import dp
from handlers import client

from utils.set_bot_commands import set_default_commands


async def on_startup(_):
    print('Бот запущен!')
    await set_default_commands(dp)


client.register_handlers_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
