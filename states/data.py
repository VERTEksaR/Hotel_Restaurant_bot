from aiogram.dispatcher.filters.state import State, StatesGroup


class UserData(StatesGroup):

    check_city = State()  # Переходной state
    check_in_date = State()  # state для подтверждения
    check_out_date = State()  # state для подтверждения
    correct_min_price = State()  # Желаемая минимальная цена
    correct_max_price = State()  # Желаемая максимальная цена
    confirm_hotel_data = State()  # state для подтверждения

    name_of_city = State()  # Название города
    geoId = State()  # id города
    latitude = State()  # Широта
    longitude = State()  # Долгота
    choice = State()  # Выбор пользователя
    check_in_year = State()  # Год заезда
    check_in_month = State()  # Месяц заезда
    check_in_day = State()  # День заезда
    check_out_year = State()  # Год выезда
    check_out_month = State()  # Месяц выезда
    check_out_day = State()  # День выезда
    rooms = State()  # Количество номеров
    adults = State()  # Количество взрослых персон
    kids = State()  # Количество детей
    min_price = State()  # Минимальная цена
    max_price = State()  # Максимальная цена
    number_of_hotels = State()  # Число отелей
    number_of_photos = State()  # Число фотографий отелей

    check_date = State()  # state для подтверждения
    confirm_restaurant_data = State()  # state для подтверждения

    visiting_rest_year = State()  # Год посещения ресторана
    visiting_rest_month = State()  # Месяц посещения ресторана
    visiting_rest_day = State()  # День посещения ресторана
    visiting_rest_hour = State()  # Час посещения ресторана
    visiting_rest_minute = State()  # Минуты посещения ресторана
    group_size = State()  # Размер группы
    number_of_restaurants = State()  # Число ресторанов
    number_of_rest_photos = State()  # Число фотографий ресторанов
