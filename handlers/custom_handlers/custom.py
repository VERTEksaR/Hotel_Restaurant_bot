from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from loader import dp
from states.data import UserData
from utils.misc import city_id, geo_cords, name_of_city
from utils import searching_hotels, searching_restaurants
from keyboards.reply import leisure, adults, kids, number_of_hotels, number_of_photo, min_price, max_price
from keyboards.reply import confirm_all_data, number_or_restaurants, number_of_rest_photos
from keyboards.inline import check_in_year, check_out_year, hotel_choice, restaurant_choice


@dp.message_handler(commands=['custom'])
async def custom_command(message: Message) -> None:
    """

    Функция, реагирующая на команду /custom. Устанавливает состояние
    для параметра name_of_city_custom, записывающий название города, введенного
    пользователем после ответа на сообщение.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел команду /custom')
    await UserData.name_of_city_custom.set()
    await message.answer('1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.name_of_city_custom)
async def set_name_city(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.name_of_city_custom.
    Записывает название города, введенного пользователем в машину состояний.
    При получении id города от функции get_city_id() записывает его в
    машину состояний. В обратном случае выводит сообщение об ошибке, и
    устанавливает состояние для параметра check_city_custom.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь ввел название города - {message.text}')
    city_name = await name_of_city.name_of_city(message)
    async with state.proxy() as data:
        data['name_of_city_custom'] = city_name
    id_of_city = await city_id.get_city_id(data['name_of_city_custom'])

    if id_of_city:
        logger.info('Обнаружен id города')
        async with state.proxy() as data:
            data['geoId_custom'] = id_of_city
        await geo_cords.set_geo_cords(state, 'custom')
        await leisure.leisure(message, 'custom')
    else:
        logger.error(f'id города {message.text} не обнаружено')
        await UserData.check_city_custom.set()
        await message.reply(f'Ошибка: города с названием {message.text} в базе нет.\n'
                            f'1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.check_city_custom)
async def wrong_city_name(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_city_custom.
    Вызывает функцию set_name_city, если предыдущее название города в базе не находилось.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    await set_name_city(message, state)


@dp.message_handler(Text(endswith='Отель'), state=UserData.choice_custom)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice_custom и
    если на кнопке было слово "Отель". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice_custom'] = message.text
    await message.answer('3. Необходимо ввести дату заезда', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text, 'custom')


@dp.message_handler(state=UserData.check_in_date_custom)
async def check_in_date(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_in_date_custom
    и вызывает функцию check_out_year.select_year() для записи
    даты отъезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел дату заезда')
    await message.answer('4. Необходимо ввести дату выезда', reply_markup=ReplyKeyboardRemove())
    await check_out_year.select_year(message, state, 'custom')


@dp.message_handler(state=UserData.check_out_date_custom)
async def check_out_date(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_out_date_custom
    и вызывает функцию hotel_choice.hotel_choice() для записи выбора сортировки отелей.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел дату выезда')
    await hotel_choice.hotel_choice(message)


@dp.message_handler(state=UserData.rooms_custom)
async def check_rooms(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.rooms_custom,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во номеров')
    async with state.proxy() as data:
        data['rooms_custom'] = message.text
    await adults.total_adults(message, state, message.text, 'custom')


@dp.message_handler(state=UserData.adults_custom)
async def check_adults(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.adults_custom,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во взрослых персон')
    async with state.proxy() as data:
        data['adults_custom'] = message.text
    await kids.total_kids(message, state, 'custom')


@dp.message_handler(state=UserData.kids_custom)
async def check_kids(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.kids_custom,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во детей')
    async with state.proxy() as data:
        data['kids_custom'] = message.text
    await UserData.min_price_custom.set()
    await min_price.set_min_price(message, 'custom')


@dp.message_handler(state=UserData.min_price_custom)
async def check_min_price(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.min_price_custom.
    Если текст сообщения - "Свой вариант", то функция устанавливает
    состояние для параметра correct_min_price_custom и уточняет желаемую сумму.
    Если пользователь нажимает на 1 из кнопок, то значения этой кнопки
    записываются в параметр min_price_custom.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    if message.text == 'Свой вариант':
        logger.info('Пользователь выбрал свой вариант минимальной цены')
        await UserData.correct_min_price_custom.set()
        await message.reply('Введите желаемую цену')
    else:
        logger.info('Пользователь ввел минимальную цену')
        async with state.proxy() as data:
            data['min_price_custom'] = message.text
        await UserData.max_price_custom.set()
        await max_price.set_max_price(message, 'custom')


@dp.message_handler(state=UserData.correct_min_price_custom)
async def correct_min_price(message: Message, state: FSMContext) -> None:
    """

    Функция, проверяющая введенную пользователем цену. Если она меньше 0,
    то минимальная цена приравнивается к 0, а затем записывается в машину
    состояний. Если больше 0 - сразу записывается. Если введенная цена не
    является целочисленным числом, то выводится ошибка с просьбой ввести
    еще раз.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    try:
        minim_price = int(message.text)
        if minim_price < 0:
            minim_price = 0
        logger.info('Пользователь ввел минимальную цену')
        async with state.proxy() as data:
            data['min_price_custom'] = minim_price
        await UserData.max_price_custom.set()
        await max_price.set_max_price(message, 'custom')
    except Exception:
        logger.error('Ошибка: цена не является целым числом')
        await UserData.correct_min_price_custom.set()
        await message.reply('Ошибка. Цена не является числом.\n'
                            'Укажите желаемую цену (руб.)')


@dp.message_handler(state=UserData.max_price_custom)
async def check_max_price(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.max_price_custom.
    Если текст сообщения - "Свой вариант", то функция устанавливает
    состояние для параметра correct_max_price_custom и уточняет желаемую сумму.
    Если пользователь нажимает на 1 из кнопок, то значения этой кнопки
    записываются в параметр max_price_custom.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    if message.text == 'Свой выбор':
        logger.info('Пользователь выбрал свой вариант максимальной цены')
        await UserData.correct_max_price_custom.set()
        await message.reply('Введите желаемую цену')
    else:
        logger.info('Пользователь ввел максимальную цену')
        async with state.proxy() as data:
            if int(data['min_price_custom']) >= int(message.text):
                data['max_price_custom'], data['min_price_custom'] = int(data['min_price_custom']) + 10000, message.text
            else:
                data['max_price_custom'] = message.text
        await number_of_hotels.set_num_of_hotels(message, 'custom')


@dp.message_handler(state=UserData.correct_max_price_custom)
async def correct_max_price(message: Message, state: FSMContext) -> None:
    """

    Функция, проверяющая введенную пользователем цену. Если она меньше
    или равно 0, то максимальная цена приравнивается к 20000,
    а затем записывается в машину состояний. Если больше 0 - сразу записывается.
    Если введенная цена не является целочисленным числом, то выводится
    ошибка с просьбой ввести еще раз.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    try:
        maxim_price = int(message.text)
        if maxim_price <= 0:
            maxim_price = 20000
        logger.info('Пользователь ввел максимальную цену')
        async with state.proxy() as data:
            if int(data['min_price_custom']) >= int(message.text):
                data['max_price_custom'], data['min_price_custom'] = int(data['min_price_custom']) + 10000, message.text
            else:
                data['max_price_custom'] = message.text
            await number_of_hotels.set_num_of_hotels(message, 'custom')
    except Exception:
        logger.error('Цена не является целым числом')
        await UserData.correct_max_price_custom.set()
        await message.reply('Ошибка. Цена не является числом.\n'
                            'Укажите желаемую цену (руб.)')


@dp.message_handler(state=UserData.number_of_hotels_custom)
async def check_num_of_hotels(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_hotels_custom,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во отелей для поиска')
    async with state.proxy() as data:
        data['number_of_hotels_custom'] = message.text
    await number_of_photo.set_num_of_photo(message, 'custom')


@dp.message_handler(state=UserData.number_of_photos_custom)
async def check_num_of_photos(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_photo_custom,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий отелей для показа')
    async with state.proxy() as data:
        data['number_of_photos_custom'] = message.text
        users_data = f'Выбранный город: {data["name_of_city_custom"]}\n' \
                     f'Ваш выбор: {data["choice_custom"]}\n' \
                     f'Дата заезда: {data["check_in_year_custom"]}-{data["check_in_month_custom"]}-' \
                     f'{data["check_in_day_custom"]}\n' \
                     f'Дата выезда: {data["check_out_year_custom"]}-{data["check_out_month_custom"]}-' \
                     f'{data["check_out_day_custom"]}\n' \
                     f'Количество номеров: {data["rooms_custom"]}\n' \
                     f'Количество взрослых персон: {data["adults_custom"]}\n' \
                     f'Количество детей: {data["kids_custom"]}\n' \
                     f'Ценовой диапазон (руб.): {data["min_price_custom"]} - {data["max_price_custom"]}\n' \
                     f'Отсортировать результаты по: {data["hotel_choice_custom_in_russian"]}'
    await message.answer('Указанные данные:\n' + users_data,
                         reply_markup=ReplyKeyboardRemove())
    await UserData.confirm_hotel_data_custom.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_hotel_data_custom)
async def show_all_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_all_data_custom.
    Вызывает функцию для поиска отелей с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_hotels.find_and_show_hotels(message, state, 'custom')


@dp.message_handler(Text(endswith='Ресторан'), state=UserData.choice_custom)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice_custom и
    если на кнопке было слово "Ресторан". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice_custom'] = message.text
    await message.answer('3. Выберите дату посещения', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text, 'custom')


@dp.message_handler(state=UserData.check_date_custom)
async def group_size(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_date_custom.
    Вызывает функцию для определения способа сортировки ресторанов.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь указал дату бронирования')
    await restaurant_choice.restaurant_choice(message)


@dp.message_handler(state=UserData.group_size_custom)
async def set_num_of_rests(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.group_size_custom.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел размер группы')
    async with state.proxy() as data:
        data['group_size_custom'] = message.text
    await number_or_restaurants.set_num_of_rests(message, 'custom')


@dp.message_handler(state=UserData.number_of_restaurants_custom)
async def set_num_of_photos(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_restaurants_custom.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во ресторанов для просмотра')
    async with state.proxy() as data:
        data['number_of_restaurants_custom'] = message.text
    await number_of_rest_photos.set_num_of_photo(message, 'custom')


@dp.message_handler(state=UserData.number_of_rest_photos_custom)
async def show_rest_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_rest_photos_custom,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий для ресторана')
    async with state.proxy() as data:
        data['number_of_rest_photos_custom'] = message.text
        user_data = f'Выбранный город: {data["name_of_city_custom"]}\n' \
                    f'Ваш выбор: {data["choice_custom"]}\n' \
                    f'Время посещения: {data["visiting_rest_year_custom"]}-{data["visiting_rest_month_custom"]}-' \
                    f'{data["visiting_rest_day_custom"]}T{data["visiting_rest_hour_custom"]}:' \
                    f'{data["visiting_rest_minute_custom"]}\n' \
                    f'Размер группы: {data["group_size_custom"]}\n' \
                    f'Отсортировать результаты: {data["restaurant_choice_custom_in_russian"]} | ' \
                    f'{data["restaurant_price_symbol"]}'
    await message.answer('Указанные данные:\n' + user_data,
                         reply_markup=ReplyKeyboardRemove())
    await UserData.confirm_restaurant_data_custom.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_restaurant_data_custom)
async def restaurant_result(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_restaurant_data_custom.
    Вызывает функцию для поиска ресторанов с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_restaurants.find_and_show_restaurants(message, state, 'custom')
