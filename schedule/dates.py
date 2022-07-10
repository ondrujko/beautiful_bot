import calendar
import datetime
from create_bot import db


async def all_actual_dates(month: int = None, year: int = None):
    """Получить список дат с завтрашнего дня и до конца месяца"""
    now = datetime.datetime.now()
    if month is None and year is None or month == now.month and year == now.year:
        month = now.month
        year = now.year
        days_in_this_month = calendar.monthrange(year, month)[1]
        list_of_days = list(range(now.day + 1, days_in_this_month + 1))
    elif month != now.month:
        days_in_this_month = calendar.monthrange(year, month)[1]
        list_of_days = list(range(1, days_in_this_month + 1))
    return list_of_days


async def get_booking_dict(month, year):
    """Получить словарь дат с информацией о статусе бронирования окон."""
    orders = await db.get_orders()
    this_month_orders = []
    for order in orders:
        if order[2] == year:
            if order[1] == month:
                this_month_orders.append(order)
    actual_days = await all_actual_dates(month, year)
    booking_dict = {}

    for day in actual_days:
        time_dict = {}
        for time in ('afternoon', 'day', 'morning'):
            time_dict[time] = False
        booking_dict[day, month, year] = time_dict
    for order in this_month_orders:
        booking_dict[day, month, year][order[3]] = True
        # [(29, 5, 2022, 'day', 222222, 1, '+375223334455', 'Примеров Пример Примерович')]
        # [(30, 5, 2022, 'day', 222222, 1, '+375223334455', 'Примеров Пример Примерович')]
    return booking_dict


async def get_booking_dict2(month, year):
    """Получить словарь дат с информацией о статусе бронирования окон."""
    booking_dict = {}
    for day in await all_actual_dates(month, year):
        time_dict = {}
        for time in ('afternoon', 'day', 'morning'):
            if await db.is_booking(day, month, year, time):
                time_dict[time] = True
            else:
                time_dict[time] = False
        booking_dict[(day, month, year)] = time_dict
    return booking_dict


async def get_free_dates(month: int, year: int, booking_dict: dict = None):
    """Получить все свободные даты в этом месяце"""
    if booking_dict is None:
        booking_dict = await get_booking_dict(month, year)
    dates = booking_dict.keys()
    approve_dates_list = []
    for date in dates:
        times = booking_dict[date].keys()
        for time in times:
            if booking_dict[date][time] is False:
                approve_dates_list.append(date)
                break
    return approve_dates_list


async def get_free_times(dd_mm_yyyy: str, booking_dict: dict = None):
    """Получить список свободных окон. """
    free_times = []
    date = tuple(map(int, dd_mm_yyyy.split(':')))
    if booking_dict is None:
        booking_dict = await get_booking_dict(date[1], date[2])

    times = booking_dict[date].keys()
    for time in times:
        time_status = booking_dict[date][time]
        if time_status is False:
            free_times.append(time)
    return free_times

