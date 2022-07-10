from aiogram import types, Dispatcher
from create_bot import bot, db
import keyboards
import materials
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime


# Последовательность шагов конечного автомата
class FSMclient(StatesGroup):
    date = State()
    time = State()
    fio = State()
    contact = State()
    confirm = State()


# Команда start или запуск бота
async def command_start(message: types.Message):
    if message.text in ['/start', '/menu']:
        await message.answer(materials.welcome_message, reply_markup=await keyboards.client_keyboard.main_menu_markup())
        await db.add_new_user(message.chat.id)

    elif message.text == '/help':
        await message.answer('Если у вас возникли вопросы напишите @ondrujko')


# Обработчик сообщения Записаться
async def new_booking(message: types.Message):
    booking_info = await db.search_booking(message.chat.id)
    if booking_info is False:
        await FSMclient.date.set()
        t1 = datetime.datetime.now()
        await message.answer('Выберите дату на которую хотите записаться\n'
                             f'Даты представлены за месяц: {materials.months[datetime.datetime.now().month]}',
                             reply_markup=await keyboards.client_keyboard.schedule_markup())
        await message.answer('Для отмены процедуры записи используйте кнопку ниже👇 или отправьте команду /cancel',
                             reply_markup=await keyboards.client_keyboard.cancel_markup())
        print('TIME:',datetime.datetime.now() - t1)
    else:
        await message.answer(
            f'У вас уже есть активная запись! Чтобы создать новую вы должны отменить предыдущую.\n\n'
            f'{await materials.make_message_from_booking_info(booking_info=booking_info, with_master_info=True)}',
            reply_markup=await keyboards.client_keyboard.my_booking_markup(booking_founded=True))


# Обработчик сообщения Мои записи
async def my_booking(message: types.Message):
    booking_info = await db.search_booking(message.chat.id)  # Проверить
    if booking_info is not False:

        await message.answer(f'У вас есть активная запись.\n\n'
                             f'{await materials.make_message_from_booking_info(booking_info, with_master_info=True)}',
                             reply_markup=await keyboards.client_keyboard.my_booking_markup(True))

    else:
        await message.answer(f'У вас нет активных записей!\n'
                             f'Чтобы начать процедуру записи нажмите на кнопку Записаться✍️ ',
                             reply_markup=await keyboards.client_keyboard.my_booking_markup(False))


# Обработчик сообщения Портфолио
async def portfolio(message: types.Message):
    await message.answer('Выберите интересующую вас категорию',
                         reply_markup=await keyboards.client_keyboard.portfolio_markup())


# Обработчик сообщения Заказать бота
async def buy_bot(message: types.Message):
    await message.answer('Заказать создание бота можно у 👉@ondrujko')


# Обработчик кнопок из меню портфолио
async def portfolio_menu(message: types.Message):
    if message.text in materials.portfolio.keys():
        media = types.MediaGroup()
        for photo in materials.portfolio[message.text]:
            media.attach_photo(photo)
        await bot.send_media_group(message.chat.id, media=media)


# Удалить бронь
async def delete_booking(message: types.Message):
    await db.delete_booking(message.chat.id)
    await message.answer('Запись была отмена.', reply_markup=await keyboards.client_keyboard.main_menu_markup())


# Обработчик сообщения /menu
async def menu(message: types.Message):
    await message.answer(materials.back_to_main_menu_message,
                         reply_markup=await keyboards.client_keyboard.main_menu_markup())


# FSM запросить нажать на inline кнопку даты
async def get_date(call: types.CallbackQuery, state: FSMclient):
    now = datetime.datetime.now()
    if call.data.startswith('month:'):
        if int(call.data.split(':')[1]) != now.month:
            await call.message.edit_text('Выберите дату на которую хотите записаться\n'
                                         f'Даты представлены за месяц: {materials.months[now.month + 1]}',

                                         reply_markup=await keyboards.client_keyboard.schedule_markup(True))
        else:
            await call.message.edit_text('Выберите дату на которую хотите записаться\n'
                                         f'Даты представлены за месяц: {materials.months[now.month]}',

                                         reply_markup=await keyboards.client_keyboard.schedule_markup())
    else:
        async with state.proxy() as data:
            data['date'] = call.data
        await bot.edit_message_text('Выберите время',
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=await keyboards.client_keyboard.time_markup(call.data))
        await FSMclient.next()
    print('TIME NEXT MONTH:', datetime.datetime.now() - now)


# FSM обработчик нажатий на inline кнопку даты
async def get_time(call: types.CallbackQuery, state: FSMclient):
    now = datetime.datetime.now()
    if call.data == 'back to calendar':
        await call.message.edit_text('Выберите дату на которую хотите записаться\n'
                                     f'Даты представлены за месяц: {materials.months[now.month]}',
                                     reply_markup=await keyboards.client_keyboard.schedule_markup())
        await FSMclient.date.set()

    else:
        async with state.proxy() as data:
            data['time'] = call.data.split(':')[-1]
            date = tuple(map(int, str(data['date']).split(':')))
            day, month, year = date[0], date[1], date[2]
            if month < 10:
                month = '0' + str(month)
            if day < 10:
                day = '0' + str(day)
            await call.message.edit_text(f'Вы начали процедуру записи на {day}.{month}.{year}\n'
                                         f'{materials.dict_time[data["time"]]}')
            await call.message.answer('Отправьте ваше ФИО')
        await FSMclient.next()


# FSM запросить ФИО
async def get_fio(message: types.Message, state: FSMclient):
    async with state.proxy() as data:
        data['fio'] = message.text
    await message.answer('Введите ваш номер телефона или нажмите на кнопку Поделиться контактом',
                         reply_markup=await keyboards.client_keyboard.share_contact_markup())
    await FSMclient.next()


# FSM запросить контакт (ввод вручную)
async def get_contact_text(message: types.Message, state: FSMclient):
    cancel_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_button = types.KeyboardButton('Отмена❌')
    cancel_keyboard.add(cancel_button)
    if message.content_type == 'text':
        async with state.proxy() as data:
            data['contact'] = message.text
    else:
        async with state.proxy() as data:
            data['contact'] = message.contact.phone_number

    async with state.proxy() as data:
        date = tuple(map(int, str(data['date']).split(':')))
        day, month, year = date[0], date[1], date[2]
        time = str(data['time']).split(':')[-1]
        contact = data['contact']
        fio = data['fio']
        d_time = {'morning': '9:00 - 11:30',
                  'day': '12:00 - 14:30',
                  'afternoon': '15:00 - 17:30'}
    if month < 10:
        month = '0' + str(month)
    await message.answer(
        f'Пожалуйста, проверьте данные, и, если заметили ошибку, то нажмите на кнопку Отмена и начните запись с '
        f'начала.\n\n'
        f'Дата: {day}.{month}.{year}\n'
        f'Время: {d_time[time]}\n'
        f'Ваше ФИО: {fio}\n'
        f'Ваш номер телефона: {contact}\n\n'
        f'Если данные введены верно нажмите кнопку Подтвердить',
        reply_markup=await keyboards.client_keyboard.confirm_booking_markup())

    msg = await message.answer('Обязательно подтвердите или отмените эту запись в ближайшее время.\n'
                               'В противном случае она будет отменена автоматически.', reply_markup=cancel_keyboard)
    async with state.proxy() as data:
        data['message_for_delete'] = msg
    await FSMclient.next()


# FSM подтверждение брони
async def confirm_booking(call: types.CallbackQuery, state: FSMclient):
    if call.data == 'confirm_booking':
        async with state.proxy() as data:
            date = tuple(map(int, str(data['date']).split(':')))
            day, month, year = date[0], date[1], date[2]
            time = str(data['time']).split(':')[-1]
            chat_id = call.message.chat.id
            status = True
            contact = data['contact']
            fio = data['fio']
            await db.add_new_order(day, month, year, time, chat_id, status, contact, fio)
            await call.message.edit_text(materials.final_booking_message)
    elif call.data == 'decline_booking':
        await call.message.edit_text('Запись была отменена.')
    await call.message.answer(materials.back_to_main_menu_message,
                              reply_markup=await keyboards.client_keyboard.main_menu_markup())
    async with state.proxy() as data:
        msg = data['message_for_delete']
        await bot.delete_message(msg.chat.id, msg.message_id)
    await state.finish()


# Остановить процедуру записи
async def fsm_stop(message: types.Message, state: FSMclient):
    await message.answer(materials.cancel_booking_procedure_message,
                         reply_markup=await keyboards.client_keyboard.main_menu_markup())
    async with state.proxy() as data:
        try:
            msg = data['message_for_delete']
            bot.delete_message(msg.message.id, msg.message.message_id)
        except:
            pass
    await state.finish()


# Регистрация хэндлеров
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help', 'menu'], state=None)
    dp.register_message_handler(fsm_stop, lambda message: message.text in ['Отмена❌', '/cancel', '/start', 'help', '/menu'], state='*')
    dp.register_callback_query_handler(get_date, state=FSMclient.date)
    dp.register_callback_query_handler(get_time, state=FSMclient.time)
    dp.register_callback_query_handler(confirm_booking, state=FSMclient.confirm)
    dp.register_message_handler(get_fio, content_types='text', state=FSMclient.fio)
    dp.register_message_handler(get_contact_text, content_types=['text', 'contact'], state=FSMclient.contact)
    dp.register_message_handler(command_start, commands=['start', 'help'], state=None)

    # Главное меню
    dp.register_message_handler(new_booking, lambda message: message.text == 'Записаться✍️')
    dp.register_message_handler(my_booking, lambda message: message.text == 'Мои записи📆')
    dp.register_message_handler(portfolio, lambda message: message.text == 'Портфолио💅🏻')
    dp.register_message_handler(buy_bot, lambda message: message.text == 'Заказать бота🦾')

    dp.register_message_handler(delete_booking, lambda message: message.text == 'Отменить запись🙅')
    dp.register_message_handler(menu, lambda message: message.text in ['Назад🔙', '/menu'])
    dp.register_message_handler(portfolio_menu, content_types='text')
