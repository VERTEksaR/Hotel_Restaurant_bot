from datetime import datetime
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from database.models import db, User, Choice
from loader import dp
from states.data import UserData
from utils.misc import city_id, geo_cords, name_of_city
from utils import searching_hotels, searching_restaurants
from keyboards.reply import leisure, rooms, adults, kids, number_of_hotels, number_of_photo
from keyboards.reply import confirm_all_data, size_group, number_or_restaurants, number_of_rest_photos
from keyboards.inline import check_in_year, check_out_year


@dp.message_handler(commands=['high'])
async def high_command(message: Message) -> None:
    """

    Функция, реагирующая на команду /high. Устанавливает состояние
    для параметра name_of_city_high, записывающий название города, введенного
    пользователем после ответа на сообщение.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел команду /high')
    await UserData.name_of_city_high.set()
    await message.answer('1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.name_of_city_high)
async def set_name_city(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.name_of_city_high.
    Записывает название города, введенного пользователем в машину состояний.
    При получении id города от функции get_city_id() записывает его в
    машину состояний. В обратном случае выводит сообщение об ошибке, и
    устанавливает состояние для параметра check_city_high.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь ввел название города - {message.text}')
    city_name = await name_of_city.name_of_city(message)
    async with state.proxy() as data:
        data['name_of_city_high'] = city_name
    id_of_city = await city_id.get_city_id(data['name_of_city_high'])

    if id_of_city:
        logger.info('Обнаружен id города')
        async with state.proxy() as data:
            data['geoId_high'] = id_of_city
        await geo_cords.set_geo_cords(state, 'high')
        await leisure.leisure(message, 'high')
    else:
        logger.error(f'id города {message.text} не обнаружено')
        await UserData.check_city_high.set()
        await message.reply(f'Ошибка: города с названием {message.text} в базе нет.\n'
                            f'1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.check_city_high)
async def wrong_city_name(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_city_high.
    Вызывает функцию set_name_city, если предыдущее название города в базе не находилось.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    await set_name_city(message, state)


@dp.message_handler(Text(endswith='Отель'), state=UserData.choice_high)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice_high и
    если на кнопке было слово "Отель". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice_high'] = message.text
    await message.answer('3. Необходимо ввести дату заезда', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text, 'high')


@dp.message_handler(state=UserData.check_in_date_high)
async def check_in_date(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_in_date_high
    и вызывает функцию check_out_year.select_year() для записи
    даты отъезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел дату заезда')
    await message.answer('4. Необходимо ввести дату выезда', reply_markup=ReplyKeyboardRemove())
    await check_out_year.select_year(message, state, 'high')


@dp.message_handler(state=UserData.check_out_date_high)
async def check_out_date(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_out_date_high
    и вызывает функцию rooms.set_rooms() для записи количества номеров.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел дату выезда')
    await rooms.set_rooms(message, 'high')


@dp.message_handler(state=UserData.rooms_high)
async def check_rooms(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.rooms_high,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во номеров')
    async with state.proxy() as data:
        data['rooms_high'] = message.text
        await adults.total_adults(message, state, message.text, 'high')


@dp.message_handler(state=UserData.adults_high)
async def check_adults(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.adults_high,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во взрослых персон')
    async with state.proxy() as data:
        data['adults_high'] = message.text
    await kids.total_kids(message, state, 'high')


@dp.message_handler(state=UserData.kids_high)
async def check_kids(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.kids_high,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во детей')
    async with state.proxy() as data:
        data['kids_high'] = message.text
    await number_of_hotels.set_num_of_hotels(message, 'high')


@dp.message_handler(state=UserData.number_of_hotels_high)
async def check_num_of_hotels(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_hotels_high,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во отелей для поиска')
    async with state.proxy() as data:
        data['number_of_hotels_high'] = message.text
    await number_of_photo.set_num_of_photo(message, 'high')


@dp.message_handler(state=UserData.number_of_photos_high)
async def check_num_of_photos(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_photo_high,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий отелей для показа')
    async with state.proxy() as data:
        data['number_of_photos_high'] = message.text
        data['min_price_high'], data['max_price_high'] = 0, 172000
        users_data = f'Выбранный город: {data["name_of_city_high"]}\n' \
                     f'Ваш выбор: {data["choice_high"]}\n' \
                     f'Дата заезда: {data["check_in_year_high"]}-{data["check_in_month_high"]}-' \
                     f'{data["check_in_day_high"]}\n' \
                     f'Дата выезда: {data["check_out_year_high"]}-{data["check_out_month_high"]}-' \
                     f'{data["check_out_day_high"]}\n' \
                     f'Количество номеров: {data["rooms_high"]}\n' \
                     f'Количество взрослых персон: {data["adults_high"]}\n' \
                     f'Количество детей: {data["kids_high"]}\n' \
                     f'Отсортировать результаты: по популярности'
    await message.answer('Указанные данные:\n' + users_data,
                         reply_markup=ReplyKeyboardRemove())

    with db:
        user = User.get_or_none(User.user_id == message.from_user.id)

        if user is None:
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            User.create(user_id=user_id, username=username, first_name=first_name)
            user = User.get_or_none(User.user_id == message.from_user.id)
        Choice.create(user=user, city=data['name_of_city_high'], command='high', choice=data['choice_high'],
                      sort='Популярность', date_of_request=datetime.now(),
                      date_of_visit=(f'{data["check_in_year_high"]}-{data["check_in_month_high"]}-'
                                     f'{data["check_in_day_high"]} -> {data["check_out_year_high"]}-'
                                     f'{data["check_out_month_high"]}-{data["check_in_day_high"]}'))

    await UserData.confirm_hotel_data_high.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_hotel_data_high)
async def show_all_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_all_data_high.
    Вызывает функцию для поиска отелей с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_hotels.find_and_show_hotels(message, state, 'high')


@dp.message_handler(Text(endswith='Ресторан'), state=UserData.choice_high)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice_high и
    если на кнопке было слово "Ресторан". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice_high'] = message.text
    await message.answer('3. Выберите дату посещения', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text, 'high')


@dp.message_handler(state=UserData.check_date_high)
async def group_size(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_date_high.
    Вызывает функцию для определения размера группы.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь указал дату бронирования')
    await size_group.set_group_size(message, 'high')


@dp.message_handler(state=UserData.group_size_high)
async def set_num_of_rests(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.group_size_high.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел размер группы')
    async with state.proxy() as data:
        data['group_size_high'] = message.text
    await number_or_restaurants.set_num_of_rests(message, 'high')


@dp.message_handler(state=UserData.number_of_restaurants_high)
async def set_num_of_photos(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_restaurants_high.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во ресторанов для просмотра')
    async with state.proxy() as data:
        data['number_of_restaurants_high'] = message.text
    await number_of_rest_photos.set_num_of_photo(message, 'high')


@dp.message_handler(state=UserData.number_of_rest_photos_high)
async def show_rest_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_rest_photos_high,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий для ресторана')
    async with state.proxy() as data:
        data['number_of_rest_photos_high'] = message.text
        user_data = f'Выбранный город: {data["name_of_city_high"]}\n' \
                    f'Ваш выбор: {data["choice_high"]}\n' \
                    f'Время посещения: {data["visiting_rest_year_high"]}-{data["visiting_rest_month_high"]}-' \
                    f'{data["visiting_rest_day_high"]}T{data["visiting_rest_hour_high"]}:' \
                    f'{data["visiting_rest_minute_high"]}\n' \
                    f'Размер группы: {data["group_size_high"]}\n' \
                    f'Отсортировать результаты: Высокая кухня'
    await message.answer('Указанные данные:\n' + user_data,
                         reply_markup=ReplyKeyboardRemove())

    with db:
        user = User.get_or_none(User.user_id == message.from_user.id)

        if user is None:
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            User.create(user_id=user_id, username=username, first_name=first_name)
            user = User.get_or_none(User.user_id == message.from_user.id)
        Choice.create(user=user, city=data['name_of_city_high'], command='high', choice=data['choice_high'],
                      sort='$$$$', date_of_request=datetime.now(),
                      date_of_visit=(f'{data["visiting_rest_year_high"]}-{data["visiting_rest_month_high"]}-'
                                     f'{data["visiting_rest_day_high"]}T{data["visiting_rest_hour_high"]}:'
                                     f'{data["visiting_rest_minute_high"]}'))

    await UserData.confirm_restaurant_data_high.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_restaurant_data_high)
async def restaurant_result(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_restaurant_data_high.
    Вызывает функцию для поиска ресторанов с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_restaurants.find_and_show_restaurants(message, state, 'high')
