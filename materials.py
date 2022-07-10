async def make_message_from_booking_info(booking_info: tuple, with_master_info: bool = False):
    day, month, year = booking_info[0], booking_info[1], booking_info[2]

    time = dict_time[booking_info[3]]
    contact = booking_info[6]
    fio = booking_info[7]

    if int(day) < 10:
        day = '0' + str(day)
    if int(month) < 10:
        month = '0' + str(month)
    message = f'Дата: {day}.{month}.{year}\n'\
              f'Время: {time}\n'\
              f'ФИО: {fio}\n'\
              f'Ваш контакт: {contact}\n'
    if with_master_info:
        message += f'Адрес мастера: ул. Мира 15, кв. 7\n' \
                   f'Контакт мастера: +375258765432'
    return message

welcome_message = """Привет, меня зовут Таня!☀️ 
Я создаю индивидуальность💡
В этом чат-боте ты можешь ознакомиться с моими работами 💅🏻 или записаться ко мне на ноготочки ✍️. 
Тебе нужно только сделать "тыц пальчиком" на кнопки ниже и вуаля ✨!"""

final_booking_message = """Отлично, ваша запись была успешно добавлена!
В ближайшее время с вами свяжется наш менеджер для окончательного подтверждения."""

back_to_main_menu_message = """Главное меню. Для взаимодействия с ботом используйте кнопки ниже👇"""

cancel_booking_procedure_message = """Процедура записи была отменена!
Чтобы начать её снова нажмите на кнопку Записаться✍️"""

main_menu_buttons = ['Записаться✍️', 'Мои записи📆', 'Портфолио💅🏻', 'Заказать бота🦾']

dict_time = {'morning': '9:00 - 11:30',
             'day': '12:00 - 14:30',
             'afternoon': '15:00 - 17:30'}

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

portfolio = {
    'Геометрия🔸': [
        'AgACAgIAAxkBAAN6YlVgiQ9ObzF1tfGUR9GYtS1143QAAoizMRtajZhIC4HGTD6PBtUBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAN7YlVgiVlsKFePLyEcws4BTO_5Zh8AAouzMRtajZhI-kuqrXYZ6wUBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAN8YlVgiTd7mW2DxIfzHvkTfdHwksEAAoyzMRtajZhIhPzEdAuhP5EBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAN-YlVgiYRMcT0XFJjauJaxitVbRfsAAo6zMRtajZhIxkqN4SYSovABAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAN9YlVgiZ5c7fXsQPYPxm-yO5XRGYoAAo2zMRtajZhIVqLTEYmiCDEBAAMCAANzAAMjBA'
    ],
    'Матовый🤍': [
        'AgACAgIAAxkBAAOFYlVhKTsyE4aA5XX25SRK4NoRoBkAAqKzMRtajZhIXBqMY-8nhjsBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOHYlVhKWWWUCIN2p3AFqXQ7qKOCVcAAqSzMRtajZhIljF6j08VWTMBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOKYlVhKf6UFA9_bSC2EZmSyqFxdzgAAqizMRtajZhI1saq6SlRhmIBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOGYlVhKWtPHMbmcdfn1WV_oHXUp7YAAqOzMRtajZhIzHMrccRz9VEBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOJYlVhKWHDv98UtALpUK5TYfPe4ggAAqezMRtajZhIsOYQmObEgW8BAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOIYlVhKT32Bo251EF2Vq4k7ViyY94AAqWzMRtajZhIMIK0TrZaH5ABAAMCAANzAAMjBA'
    ],
    'Втирка🔥': [
        'AgACAgIAAxkBAAOSYlVhjM6CtsaL5n1j6Xzaw7fAdRAAAuCzMRtajZhIcMiXKYOCWEABAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOVYlVhjNL9b0Y9Z6f-lzkfR4ycJ8IAAuKzMRtajZhILyg3h8_9bcYBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOYYlVhjDPSKwQV_DZ3qze-t39jmC8AAuazMRtajZhI7025Fo0InzwBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOTYlVhjKE-fm86WqRWhRwCptXkBmcAAuGzMRtajZhItUOjqgaHu3kBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOZYlVhjEsp7w9vsM3WcQIuksMb0ssAAuezMRtajZhIdFrffpCkh3cBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOWYlVhjMfDyInY4umfiNh81cPe5fAAAuOzMRtajZhIxwjDxXJVhmMBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOUYlVhjBC8HROP7PSHvwRPpoRbm_AAAuKzMRtajZhILyg3h8_9bcYBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOXYlVhjKFOMbG9LyF3Slgvh-rNprsAAuWzMRtajZhIgAVkgXx3Ge4BAAMCAANzAAMjBA'
    ],
    'Мрамор◽️': [
        'AgACAgIAAxkBAAOjYlViDVBQqwVwaDcAAffArCcLLvsBAALYszEbWo2YSO1qacZeZqidAQADAgADcwADIwQ',
        'AgACAgIAAxkBAAOpYlViDcyUO96v0_k0zPMwWlmxYyIAAt-zMRtajZhIGDIBkHbhgM8BAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOoYlViDfi53wPOaWAtqDH8VUsyZqcAAt6zMRtajZhIeTy9D29Na9YBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOkYlViDdTS2u-tWbC0OimN1DuTdHwAAtmzMRtajZhIt9pf3b4K6cYBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOmYlViDXpMGvLJPmVZ-5xgPs3uA2MAAtyzMRtajZhIkAcHg9tH8yQBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOlYlViDTh7hWcPcpntcNzSdqfq6xgAAtuzMRtajZhIZkIuCLRsn6EBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOnYlViDcDvEQro7hjD9G4UDa6bwcQAAt2zMRtajZhI-H3w4rfKtvIBAAMCAANzAAMjBA',
    ],
    'Французский🌸': [
        'AgACAgIAAxkBAAOyYlVikUtAu4ZFqUhW7zJylyZQbqIAApazMRtajZhIGg-AwXM787QBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAO0YlVikQuDZdRgr-XwSI6qAn9CVW0AApizMRtajZhI21kK_QqdOV0BAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAO4YlVikQnlla-A-TQCmoMAAf7z-yU0AAKcszEbWo2YSGtlX9WUVYLKAQADAgADcwADIwQ',
        'AgACAgIAAxkBAAO5YlVikRouad4fWBaPjigOQK6Q9IAAApyzMRtajZhIa2Vf1ZRVgsoBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAOzYlVikVEZx_JWFGpd-V-UoEi7g8EAApezMRtajZhIcUPBtvdxo0EBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAO1YlVikaNCP2m28-3v2Fl3hMwjRWAAApmzMRtajZhIfofYW28yB_QBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAO3YlVikch6IPqitidrtX0XKIZF1ZkAApqzMRtajZhIKzRS2gMhJy8BAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAO2YlVikYZubYDeJPctrL_E5iYsbjMAApmzMRtajZhIfofYW28yB_QBAAMCAANzAAMjBA'
    ],
    'Кошачий глаз🐱': [
        'AgACAgIAAxkBAAPDYlVjFaOo6f1mTWMIJk2Juhw3AAFUAALqszEbWo2YSDtXhtH3_SeJAQADAgADcwADIwQ',
        'AgACAgIAAxkBAAPEYlVjFa566Gmp1Qy00HUAAS0IvX0eAALrszEbWo2YSJXF59pJ44eOAQADAgADcwADIwQ',
        'AgACAgIAAxkBAAPIYlVjFd69QCe4cDM-5s_cYc-8CMkAAvSzMRtajZhIAAGinV7-cq3OAQADAgADcwADIwQ',
        'AgACAgIAAxkBAAPHYlVjFdizrXm4op6cNf00TDsSCAIAAvCzMRtajZhIcvjIXqFg5V4BAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPFYlVjFZB5n13-E_V1rrYtHa8ZjMwAAuyzMRtajZhI8EMUXtCLAXEBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPGYlVjFbra86bKNzo9bSxszd-65GIAAu-zMRtajZhIzmmWIlBHSGABAAMCAANzAAMjBA'
    ],
    'Блесточки ✨': [
        'AgACAgIAAxkBAAPQYlVjX0FD1Ky-kS3Mwih3A4oBJpwAAvizMRtajZhI-VrlG8mUbZIBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPSYlVjX1Ughtjp2hnEnTiCXaqksZ0AAvqzMRtajZhILs275D2dyvkBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPRYlVjX3i_31s2m5s25-w_mOAL8LQAAvmzMRtajZhInvr6QcX9mJUBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPUYlVjX4mPdkO9vPDiPcHtEbBcQRgAAv2zMRtajZhIZZ1KApwq_QMBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPTYlVjX0BuoZ9SG0RyOkHYVakEhykAAvyzMRtajZhITeuiaHWYbWYBAAMCAANzAAMjBA'
    ],
    'Кружево💫': [
        'AgACAgIAAxkBAAPjYlVkHV0GHEqVzsY4LfonvZpQanwAArWzMRtajZhITc7CRNJVfMoBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPlYlVkHXzKM0lJ-rCtT-VNWUCO_hsAArezMRtajZhIECevLF9hcUoBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPmYlVkHSKXMEEZTa7D4V05_lhl79wAArizMRtajZhIx7gwFj_9wsABAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPpYlVkHeYE-AG5yImxxcqwPlvw5PoAAruzMRtajZhIA8o8lfiTz7cBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPnYlVkHSuu2gvFNOF6Ewq6u-mADnkAArmzMRtajZhIgQT5gG38dugBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPoYlVkHYF6-viaGRDvTjCqyiIFPmsAArqzMRtajZhIuBTaZTM-J3UBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPkYlVkHXnimFCxu0V4JwlWsz4OIdoAArazMRtajZhIcyrZ551ELXYBAAMCAANzAAMjBA'
    ],
    'Градиент🌈': [
        'AgACAgIAAxkBAAPxYlVkvNwAASm3MwGC4SSIx3wJq_SlAALBszEbWo2YSDHfQCE-mKJaAQADAgADcwADIwQ',
        'AgACAgIAAxkBAAPyYlVkvPUxGn1Ny-Hk9NQsmX26NDIAAsOzMRtajZhIrhyYy8i_YjUBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAPzYlVkvMU_YXc4YnTBK-CtbsXkPtkAAsSzMRtajZhISb5icI6ziy0BAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAP1YlVkvPu2RcGFgEdvrd78ypR4BSQAAtGzMRtajZhIdgo9Ox7EN-IBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAP0YlVkvKvBM5f_HEJQ7VnQ_ohEiEsAAtCzMRtajZhI15TP04W_6PUBAAMCAANzAAMjBA',
    ],
    'Паутинка🕸': [
        'AgACAgIAAxkBAAP8YlVk_jUaKevoie3fxXokIYKyFsoAApGzMRtajZhItmaP964D_7kBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAP_YlVk_o6vuHcKFCIu9Wcch3VOP_AAApSzMRtajZhI_l-FVDIB7UUBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAP-YlVk_jYa4xjb_MYv7JvY98PBt6kAApOzMRtajZhI5GgeNSSjr9cBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAIBAAFiVWT-0ycr69vQTF8AARIKUFj53iEAApWzMRtajZhI4mS_m3q_FBUBAAMCAANzAAMjBA',
        'AgACAgIAAxkBAAP9YlVk_sspXHho0Kn7aRuCcNBUDmcAApKzMRtajZhI3eyycthzIuQBAAMCAANzAAMjBA'
    ]
}
