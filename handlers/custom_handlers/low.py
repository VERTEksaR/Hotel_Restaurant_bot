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
    для параметра name_of_city, записывающий название города, введенного
    пользователем после ответа на сообщение.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел команду /low')
    await UserData.name_of_city.set()
    await message.answer('1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.name_of_city)
async def set_name_city(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.name_of_city.
    Записывает название города, введенного пользователем в машину состояний.
    При получении id города от функции get_city_id() записывает его в
    машину состояний. В обратном случае выводит сообщение об ошибке, и
    устанавливает состояние для параметра check_city.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь ввел название города - {message.text}')
    async with state.proxy() as data:
        data['name_of_city'] = message.text
    id_of_city = await city_id.get_city_id(data['name_of_city'], message)

    if id_of_city:
        logger.info('Обнаружен id города')
        async with state.proxy() as data:
            data['geoId'] = id_of_city
        await geo_cords.set_geo_cords(state)
        await leisure.leisure(message)
    else:
        logger.error(f'id города {message.text} не обнаружено')
        await UserData.check_city.set()
        await message.reply(f'Ошибка: города с названием {message.text} в базе нет.\n'
                            f'1. Пожалуйста, введите название города')


@dp.message_handler(state=UserData.check_city)
async def wrong_city_name(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_city.
    Вызывает функцию set_name_city, если предыдущее название города в базе не находилось.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    await set_name_city(message, state)


@dp.message_handler(Text(endswith='Отель'), state=UserData.choice)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice и
    если на кнопке было слово "Отель". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice'] = message.text
    await message.answer('3. Необходимо ввести дату заезда', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text)


@dp.message_handler(state=UserData.check_in_date)
async def check_in_date(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_in_date
    и вызывает функцию check_out_year.select_year() для записи
    даты отъезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел дату заезда')
    await message.answer('4. Необходимо ввести дату выезда', reply_markup=ReplyKeyboardRemove())
    await check_out_year.select_year(message, state)


@dp.message_handler(state=UserData.check_out_date)
async def check_out_date(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_out_date
    и вызывает функцию rooms.set_rooms() для записи количества номеров.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь ввел дату выезда')
    await rooms.set_rooms(message)


@dp.message_handler(state=UserData.rooms)
async def check_rooms(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.rooms,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во номеров')
    async with state.proxy() as data:
        data['rooms'] = message.text
        await adults.total_adults(message, state, message.text)


@dp.message_handler(state=UserData.adults)
async def check_adults(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.adults,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во взрослых персон')
    async with state.proxy() as data:
        data['adults'] = message.text
    await kids.total_kids(message, state)


@dp.message_handler(state=UserData.kids)
async def check_kids(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.kids,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во детей')
    async with state.proxy() as data:
        data['kids'] = message.text
    await min_price.set_min_price(message)


@dp.message_handler(state=UserData.min_price)
async def check_min_price(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.min_price.
    Если текст сообщения - "Свой вариант", то функция устанавливает
    состояние для параметра correct_min_price и уточняет желаемую сумму.
    Если пользователь нажимает на 1 из кнопок, то значения этой кнопки
    записываются в параметр min_price.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    if message.text == 'Свой вариант':
        logger.info('Пользователь выбрал свой вариант минимальной цены')
        await UserData.correct_min_price.set()
        await message.reply('Введите желаемую цену')
    else:
        logger.info('Пользователь ввел минимальную цену')
        async with state.proxy() as data:
            data['min_price'] = message.text
        await max_price.set_max_price(message)


@dp.message_handler(state=UserData.correct_min_price)
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
            data['min_price'] = minim_price
        await max_price.set_max_price(message)
    except Exception:
        logger.error('Цена не является целым числом')
        await UserData.correct_min_price.set()
        await message.reply('Ошибка. Цена не является числом.\n'
                            'Укажите желаемую цену (руб.)')


@dp.message_handler(state=UserData.max_price)
async def check_max_price(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.max_price.
    Если текст сообщения - "Свой вариант", то функция устанавливает
    состояние для параметра correct_max_price и уточняет желаемую сумму.
    Если пользователь нажимает на 1 из кнопок, то значения этой кнопки
    записываются в параметр max_price.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    if message.text == 'Свой вариант':
        logger.info('Пользователь выбрал свой вариант максимальной цены')
        await UserData.correct_max_price.set()
        await message.reply('Введите желаемую цену')
    else:
        logger.info('Пользователь ввел максимальную цену')
        async with state.proxy() as data:
            data['max_price'] = message.text
        await number_of_hotels.set_num_of_hotels(message)


@dp.message_handler(state=UserData.correct_max_price)
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
            data['max_price'] = maxim_price
            await number_of_hotels.set_num_of_hotels(message)
    except Exception:
        logger.error('Цена не является целым числом')
        await UserData.correct_max_price.set()
        await message.reply('Ошибка. Цена не является числом.\n'
                            'Укажите желаемую цену (руб.)')


@dp.message_handler(state=UserData.number_of_hotels)
async def check_num_of_hotels(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_hotels,
    записывающая выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во отелей для поиска')
    async with state.proxy() as data:
        data['number_of_hotels'] = message.text
    await number_of_photo.set_num_of_photo(message)


@dp.message_handler(state=UserData.number_of_photos)
async def check_num_of_photo(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_photo,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий отелей для показа')
    async with state.proxy() as data:
        data['number_of_photos'] = message.text
        users_data = f'Выбранный город: {data["name_of_city"]}\n' \
                     f'Ваш выбор: {data["choice"]}\n' \
                     f'Дата заезда: {data["check_in_year"]}-{data["check_in_month"]}-{data["check_in_day"]}\n' \
                     f'Дата выезда: {data["check_out_year"]}-{data["check_out_month"]}-{data["check_out_day"]}\n' \
                     f'Количество номеров: {data["rooms"]}\n' \
                     f'Количество взрослых персон: {data["adults"]}\n' \
                     f'Количество детей: {data["kids"]}\n' \
                     f'Ценовой диапазон (руб.): {data["min_price"]} - {data["max_price"]}\n' \
                     f'Отсортировать результаты: мин. - макс. цена'
    await message.answer('Указанные данные:\n' + users_data,
                         reply_markup=ReplyKeyboardRemove())
    await UserData.confirm_hotel_data.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_hotel_data)
async def show_all_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_all_data.
    Вызывает функцию для поиска отелей с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_hotels.find_and_show_hotels(message, state)


@dp.message_handler(Text(endswith='Ресторан'), state=UserData.choice)
async def set_leisure(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.choice и
    если на кнопке было слово "Ресторан". Записывает данный выбор
    пользователя в машину состояний и вызывает функцию
    check_in_year.select_year() для записи даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info(f'Пользователь выбрал {message.text}')
    async with state.proxy() as data:
        data['choice'] = message.text
    await message.answer('3. Выберите дату посещения', reply_markup=ReplyKeyboardRemove())
    await check_in_year.select_year(message, message.text)


@dp.message_handler(state=UserData.check_date)
async def group_size(message: Message) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.check_date.
    Вызывает функцию для определения размера группы.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    logger.info('Пользователь указал дату бронирования')
    await size_group.set_group_size(message)


@dp.message_handler(state=UserData.group_size)
async def set_num_of_rests(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.group_size.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел размер группы')
    async with state.proxy() as data:
        data['group_size'] = message.text
    await number_or_restaurants.set_num_of_rests(message)


@dp.message_handler(state=UserData.number_of_restaurants)
async def set_num_of_photos(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_restaurants.
    Записывает выбор пользователя в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во ресторанов для просмотра')
    async with state.proxy() as data:
        data['number_of_restaurants'] = message.text
    await number_of_rest_photos.set_num_of_photo(message)


@dp.message_handler(state=UserData.number_of_rest_photos)
async def show_rest_data(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.number_of_rest_photos,
    записывающая выбор пользователя в машину состояний, а затем выводит
    данные, введенные пользователем.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    logger.info('Пользователь ввел кол-во фотографий для ресторана')
    async with state.proxy() as data:
        data['number_of_rest_photos'] = message.text
        user_data = f'Выбранный город: {data["name_of_city"]}\n' \
                    f'Ваш выбор: {data["choice"]}\n' \
                    f'Время посещения: {data["visiting_rest_year"]}-{data["visiting_rest_month"]}-' \
                    f'{data["visiting_rest_day"]}T{data["visiting_rest_hour"]}:{data["visiting_rest_minute"]}\n' \
                    f'Размер группы: {data["group_size"]}\n' \
                    f'Отсортировать результаты: Дешевое питание'
    await message.answer('Указанные данные:\n' + user_data,
                         reply_markup=ReplyKeyboardRemove())
    await UserData.confirm_restaurant_data.set()
    await confirm_all_data.confirmation(message)


@dp.message_handler(state=UserData.confirm_restaurant_data)
async def restaurant_result(message: Message, state: FSMContext) -> None:
    """

    Функция, реагирующая на изменения состояния UserData.confirm_restaurant_data.
    Вызывает функцию для поиска ресторанов с помощью API.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    await searching_restaurants.find_and_show_restaurants(message, state)
