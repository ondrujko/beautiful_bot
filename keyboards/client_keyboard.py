from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import datetime
from aiogram import types
from schedule import dates

months = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}


async def schedule_markup(next_month: bool = False):
    now = datetime.datetime.now()
    month = now.month + next_month
    if month <= 12:
        year = now.year
    else:
        month = month % 12
        year = now.year + 1
    lst = await dates.get_free_dates(month, year)
    buttons = []
    keyboard = types.InlineKeyboardMarkup(row_width=6)
    for date in lst:
        callback = f'{date[0]}:{date[1]}:{date[2]}'
        button = types.InlineKeyboardButton(text=str(date[0]), callback_data=callback)
        buttons.append(button)
    keyboard.add(*buttons)

    if next_month:
        keyboard.add(types.InlineKeyboardButton(f'<< {months[month - 1]}', callback_data=f'month:{month - 1}'))
    else:
        keyboard.add(types.InlineKeyboardButton(f'>> {months[month + 1]}', callback_data=f'month:{month + 1}'))

    return keyboard


async def time_markup(date: str):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    free_times = await dates.get_free_times(date)
    if 'morning' in free_times:
        keyboard.add(types.InlineKeyboardButton(text='9:00 - 11:30', callback_data=date + ':morning'))
    if 'day' in free_times:
        keyboard.add(types.InlineKeyboardButton(text='12:00 - 14:30', callback_data=date + ':day'))
    if 'afternoon' in free_times:
        keyboard.add(types.InlineKeyboardButton(text='15:00 - 17:30', callback_data=date + ':afternoon'))
    keyboard.add(types.InlineKeyboardButton(text='Выбрать другой день', callback_data='back to calendar'))
    return keyboard


async def main_menu_markup():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ['Записаться✍️', 'Мои записи📆', 'Портфолио💅🏻', 'Заказать бота🦾']
    keyboard.add(*buttons)
    return keyboard


async def portfolio_markup():
    keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    buttons = ['Геометрия🔸', 'Матовый🤍', 'Втирка🔥', 'Мрамор◽️', 'Французский🌸', 'Кошачий глаз🐱', 'Блесточки ✨',
               'Кружево💫', 'Градиент🌈', 'Паутинка🕸']
    keyboard.add(*buttons)
    keyboard.add('Назад🔙')
    return keyboard


async def confirm_booking_markup():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='decline_booking'),
                 types.InlineKeyboardButton(text='Подтвердить', callback_data='confirm_booking'))
    return keyboard


async def my_booking_markup(booking_founded: bool = False):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if booking_founded:
        keyboard.add('Отменить запись🙅')
    else:
        keyboard.add('Записаться✍️')
    keyboard.add('Назад🔙')
    return keyboard


async def share_contact_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    send_contact_button = types.KeyboardButton('Поделиться контактом', request_contact=True)
    cancel_button = types.KeyboardButton('Отмена❌')
    keyboard.add(send_contact_button, cancel_button)
    return keyboard


async def cancel_markup():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена❌')
