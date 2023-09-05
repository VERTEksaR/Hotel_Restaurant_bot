from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loguru import logger

from loader import dp
from states.data import UserData
from utils.misc import city_id, geo_cords
from utils import searching_hotels, searching_restaurants
from keyboards.reply import leisure, rooms, adults, kids, min_price, max_price, number_of_hotels, number_of_photo
from keyboards.reply import confirm_all_data, size_group, number_or_restaurants, number_of_rest_photos
from keyboards.inline import check_in_year, check_out_year


@dp.message_handler(commands=['low'])
async def low_command(message: Message) -> None:
    """

    Функция, реагирующая на команду /low. Устанавливает состояние
    для параметра name_of_city_low, записывающий название города, введенного
    пользователем после ответа на сообщение.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел команду /low')
    await UserData.name_of_city_low.set()
    await message.answer('1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.name_of_city_low)
async def set_name_city(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.name_of_city_low.
    Записывает название города, введенного пользователем в машину состояний.
    При получении id города от функции get_city_id() записывает его в
    машину состояний. В обратном случае выводит сообщение об ошибке, и
    устанавливает состояние для параметра check_city_low.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь ввел название города - {message.text}')
    async with state.proxy() as data:
        data['name_of_city_low'] = message.text
    id_of_city = await city_id.get_city_id(data['name_of_city_low'], message)

    if id_of_city:
        logger.info('Обнаружен id города')
        async with state.proxy() as data:
            data['geoId_low'] = id_of_city
        await geo_cords.set_geo_cords(state, 'low')
        await leisure.leisure(message, 'low')
    else:
        logger.error(f'id города {message.text} не обнаружено')
        await UserData.check_city_low.set()
        await message.reply(f'Ошибка: города с названием {message.text} в базе нет.\n'
                            f'1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.check_city_low)
async def wrong_city_name(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_city_low.
    Вызывает функцию set_name_city, если предыдущее название города в базе не находилось.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    await set_name_city(message, state)


@dp.message_handler(Text(endswith='Отель'), state=UserData.choice_low)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice_low и
    если на кнопке было слово "Отель". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice_low'] = message.text
    await message.answer('3. Необходимо ввести дату заезда', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text, 'low')


@dp.message_handler(state=UserData.check_in_date_low)
async def check_in_date(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_in_date_low
    и вызывает функцию check_out_year.select_year() для записи
    даты отъезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел дату заезда')
    await message.answer('4. Необходимо ввести дату выезда', reply_markup=ReplyKeyboardRemove())
    await check_out_year.select_year(message, state, 'low')


@dp.message_handler(state=UserData.check_out_date_low)
async def check_out_date(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_out_date_low
    и вызывает функцию rooms.set_rooms() для записи количества номеров.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел дату выезда')
    await rooms.set_rooms(message, 'low')


@dp.message_handler(state=UserData.rooms_low)
async def check_rooms(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.rooms_low,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во номеров')
    async with state.proxy() as data:
        data['rooms_low'] = message.text
        await adults.total_adults(message, state, message.text, 'low')


@dp.message_handler(state=UserData.adults_low)
async def check_adults(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.adults_low,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во взрослых персон')
    async with state.proxy() as data:
        data['adults_low'] = message.text
    await kids.total_kids(message, state, 'low')


@dp.message_handler(state=UserData.kids_low)
async def check_kids(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.kids_low,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во детей')
    async with state.proxy() as data:
        data['kids_low'] = message.text
    await min_price.set_min_price(message)


@dp.message_handler(state=UserData.min_price_low)
async def check_min_price(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.min_price_low.
    Если текст сообщения - "Свой вариант", то функция устанавливает
    состояние для параметра correct_min_price_low и уточняет желаемую сумму.
    Если пользователь нажимает на 1 из кнопок, то значения этой кнопки
    записываются в параметр min_price_low.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    if message.text == 'Свой вариант':
        logger.info('Пользователь выбрал свой вариант минимальной цены')
        await UserData.correct_min_price_low.set()
        await message.reply('Введите желаемую цену')
    else:
        logger.info('Пользователь ввел минимальную цену')
        async with state.proxy() as data:
            data['min_price_low'] = message.text
        await max_price.set_max_price(message)


@dp.message_handler(state=UserData.correct_min_price_low)
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
            data['min_price_low'] = minim_price
        await max_price.set_max_price(message)
    except Exception:
        logger.error('Цена не является целым числом')
        await UserData.correct_min_price_low.set()
        await message.reply('Ошибка. Цена не является числом.\n'
                            'Укажите желаемую цену (руб.)')


@dp.message_handler(state=UserData.max_price_low)
async def check_max_price(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.max_price_low.
    Если текст сообщения - "Свой вариант", то функция устанавливает
    состояние для параметра correct_max_price_low и уточняет желаемую сумму.
    Если пользователь нажимает на 1 из кнопок, то значения этой кнопки
    записываются в параметр max_price_low.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    if message.text == 'Свой вариант':
        logger.info('Пользователь выбрал свой вариант максимальной цены')
        await UserData.correct_max_price_low.set()
        await message.reply('Введите желаемую цену')
    else:
        logger.info('Пользователь ввел максимальную цену')
        async with state.proxy() as data:
            data['max_price_low'] = message.text
        await number_of_hotels.set_num_of_hotels(message, 'low')


@dp.message_handler(state=UserData.correct_max_price_low)
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
            data['max_price_low'] = maxim_price
            await number_of_hotels.set_num_of_hotels(message, 'low')
    except Exception:
        logger.error('Цена не является целым числом')
        await UserData.correct_max_price_low.set()
        await message.reply('Ошибка. Цена не является числом.\n'
                            'Укажите желаемую цену (руб.)')


@dp.message_handler(state=UserData.number_of_hotels_low)
async def check_num_of_hotels(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_hotels_low,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во отелей для поиска')
    async with state.proxy() as data:
        data['number_of_hotels_low'] = message.text
    await number_of_photo.set_num_of_photo(message, 'low')


@dp.message_handler(state=UserData.number_of_photos_low)
async def check_num_of_photo(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_photo_low,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий отелей для показа')
    async with state.proxy() as data:
        data['number_of_photos_low'] = message.text
        users_data = f'Выбранный город: {data["name_of_city_low"]}\n' \
                     f'Ваш выбор: {data["choice_low"]}\n' \
                     f'Дата заезда: {data["check_in_year_low"]}-{data["check_in_month_low"]}-' \
                     f'{data["check_in_day_low"]}\n' \
                     f'Дата выезда: {data["check_out_year_low"]}-{data["check_out_month_low"]}-' \
                     f'{data["check_out_day_low"]}\n' \
                     f'Количество номеров: {data["rooms_low"]}\n' \
                     f'Количество взрослых персон: {data["adults_low"]}\n' \
                     f'Количество детей: {data["kids_low"]}\n' \
                     f'Ценовой диапазон (руб.): {data["min_price_low"]} - {data["max_price_low"]}\n' \
                     f'Отсортировать результаты: мин. - макс. цена'
    await message.answer('Указанные данные:\n' + users_data,
                         reply_markup=ReplyKeyboardRemove())
    await UserData.confirm_hotel_data_low.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_hotel_data_low)
async def show_all_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_all_data_low.
    Вызывает функцию для поиска отелей с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_hotels.find_and_show_hotels(message, state, 'low')


@dp.message_handler(Text(endswith='Ресторан'), state=UserData.choice_low)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice_low и
    если на кнопке было слово "Ресторан". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice_low'] = message.text
    await message.answer('3. Выберите дату посещения', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text, 'low')


@dp.message_handler(state=UserData.check_date_low)
async def group_size(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_date_low.
    Вызывает функцию для определения размера группы.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь указал дату бронирования')
    await size_group.set_group_size(message, 'low')


@dp.message_handler(state=UserData.group_size_low)
async def set_num_of_rests(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.group_size_low.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел размер группы')
    async with state.proxy() as data:
        data['group_size_low'] = message.text
    await number_or_restaurants.set_num_of_rests(message, 'low')


@dp.message_handler(state=UserData.number_of_restaurants_low)
async def set_num_of_photos(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_restaurants_low.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во ресторанов для просмотра')
    async with state.proxy() as data:
        data['number_of_restaurants_low'] = message.text
    await number_of_rest_photos.set_num_of_photo(message, 'low')


@dp.message_handler(state=UserData.number_of_rest_photos_low)
async def show_rest_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_rest_photos_low,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий для ресторана')
    async with state.proxy() as data:
        data['number_of_rest_photos_low'] = message.text
        user_data = f'Выбранный город: {data["name_of_city_low"]}\n' \
                    f'Ваш выбор: {data["choice_low"]}\n' \
                    f'Время посещения: {data["visiting_rest_year_low"]}-{data["visiting_rest_month_low"]}-' \
                    f'{data["visiting_rest_day_low"]}T{data["visiting_rest_hour_low"]}:' \
                    f'{data["visiting_rest_minute_low"]}\n' \
                    f'Размер группы: {data["group_size_low"]}\n' \
                    f'Отсортировать результаты: Дешевое питание'
    await message.answer('Указанные данные:\n' + user_data,
                         reply_markup=ReplyKeyboardRemove())
    await UserData.confirm_restaurant_data_low.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_restaurant_data_low)
async def restaurant_result(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_restaurant_data_low.
    Вызывает функцию для поиска ресторанов с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_restaurants.find_and_show_restaurants(message, state, 'low')
