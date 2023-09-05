from aiogram.dispatcher.filters.state import State, StatesGroup


class UserData(StatesGroup):

    # Команда low (Отели)
    check_city_low = State()  # Переходной state
    check_in_date_low = State()  # state для подтверждения
    check_out_date_low = State()  # state для подтверждения
    correct_min_price_low = State()  # Желаемая минимальная цена
    correct_max_price_low = State()  # Желаемая максимальная цена
    confirm_hotel_data_low = State()  # state для подтверждения

    name_of_city_low = State()  # Название города
    geoId_low = State()  # id города
    latitude = State()  # Широта
    longitude = State()  # Долгота
    choice_low = State()  # Выбор пользователя
    check_in_year_low = State()  # Год заезда
    check_in_month_low = State()  # Месяц заезда
    check_in_day_low = State()  # День заезда
    check_out_year_low = State()  # Год выезда
    check_out_month_low = State()  # Месяц выезда
    check_out_day_low = State()  # День выезда
    rooms_low = State()  # Количество номеров
    adults_low = State()  # Количество взрослых персон
    kids_low = State()  # Количество детей
    min_price_low = State()  # Минимальная цена
    max_price_low = State()  # Максимальная цена
    number_of_hotels_low = State()  # Число отелей
    number_of_photos_low = State()  # Число фотографий отелей

    # Команда low (Рестораны)
    check_date_low = State()  # state для подтверждения
    confirm_restaurant_data_low = State()  # state для подтверждения

    visiting_rest_year_low = State()  # Год посещения ресторана
    visiting_rest_month_low = State()  # Месяц посещения ресторана
    visiting_rest_day_low = State()  # День посещения ресторана
    visiting_rest_hour_low = State()  # Час посещения ресторана
    visiting_rest_minute_low = State()  # Минуты посещения ресторана
    group_size_low = State()  # Размер группы
    number_of_restaurants_low = State()  # Число ресторанов
    number_of_rest_photos_low = State()  # Число фотографий ресторанов

    # Команда high (Отели)
    check_city_high = State()  # Переходной state
    check_in_date_high = State()  # state для подтверждения
    check_out_date_high = State()  # state для подтверждения
    correct_min_price_high = State()  # Желаемая минимальная цена
    correct_max_price_high = State()  # Желаемая максимальная цена
    confirm_hotel_data_high = State()  # state для подтверждения

    name_of_city_high = State()  # Название города
    geoId_high = State()  # id города
    choice_high = State()  # Выбор пользователя
    check_in_year_high = State()  # Год заезда
    check_in_month_high = State()  # Месяц заезда
    check_in_day_high = State()  # День заезда
    check_out_year_high = State()  # Год выезда
    check_out_month_high = State()  # Месяц выезда
    check_out_day_high = State()  # День выезда
    rooms_high = State()  # Количество номеров
    adults_high = State()  # Количество взрослых персон
    kids_high = State()  # Количество детей
    min_price_high = State()  # Минимальная цена
    max_price_high = State()  # Максимальная цена
    number_of_hotels_high = State()  # Число отелей
    number_of_photos_high = State()  # Число фотографий отелей

    # Команда high (Рестораны)
    check_date_high = State()  # state для подтверждения
    confirm_restaurant_data_high = State()  # state для подтверждения

    visiting_rest_year_high = State()  # Год посещения ресторана
    visiting_rest_month_high = State()  # Месяц посещения ресторана
    visiting_rest_day_high = State()  # День посещения ресторана
    visiting_rest_hour_high = State()  # Час посещения ресторана
    visiting_rest_minute_high = State()  # Минуты посещения ресторана
    group_size_high = State()  # Размер группы
    number_of_restaurants_high = State()  # Число ресторанов
    number_of_rest_photos_high = State()  # Число фотографий ресторанов
