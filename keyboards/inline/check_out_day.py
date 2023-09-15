from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.data import UserData
from keyboards.reply.confirmation_date import confirmation


async def filling_buttons(message: Message, day: int, total_days: int) -> None:
    """

    Функция, генерирующая inline-кнопки с днями, указывающими
    когда можно выехать из отеля.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param day: (int) день заселения или первый день месяца;
    :param total_days: (int) оставшиеся дни для выбора в месяце.
    :return: None

    """
    day_button = InlineKeyboardMarkup(row_width=7)
    for days in range(day, total_days):
        day_button.insert(InlineKeyboardButton(text=f'{days}', callback_data=str(days)))
    await message.answer('Выберите день:', reply_markup=day_button)


async def select_day(message: Message, state: FSMContext, month: str, function: str) -> None:
    """

    Функция, задающая параметры day и total_days для функции filling_buttons().
    Устанавливает состояние для параметра check_out_day, записывающий день выезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param month: (str) месяц выезда;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    async with state.proxy() as data:
        data_crit = f'_{function}'
        check_in_year = int(data[f'check_in_year{data_crit}'])
        check_in_month = int(data[f'check_in_month{data_crit}'])
        check_in_day = int(data[f'check_in_day{data_crit}'])
        check_out_month = int(month)

        if check_out_month == check_in_month:
            if check_out_month in [1, 3, 5, 7, 8, 10, 12]:
                await filling_buttons(message, check_in_day + 1, 32)
            elif check_out_month in [4, 6, 9, 11]:
                await filling_buttons(message, check_in_day + 1, 31)
            elif (check_out_month == 2) and (check_in_year % 4 == 0):
                await filling_buttons(message, check_in_day + 1, 30)
            elif (check_out_month == 2) and (check_in_year % 4 != 0):
                await filling_buttons(message, check_in_day + 1, 29)
        else:
            if check_out_month in [1, 3, 5, 7, 8, 10, 12]:
                await filling_buttons(message, 1, check_in_day + 1)
            elif check_out_month in [4, 6, 9, 11]:
                await filling_buttons(message, 1, check_in_day)
            elif (check_out_month == 2) and (check_in_year % 4 == 0):
                await filling_buttons(message, 1, check_in_day)
            elif (check_out_month == 2) and (check_in_year % 4 != 0):
                await filling_buttons(message, 1, check_in_day + 1)

    if function == 'low':
        await UserData.check_out_day_low.set()
    elif function == 'high':
        await UserData.check_out_day_high.set()
    elif function == 'custom':
        await UserData.check_out_day_custom.set()


@dp.callback_query_handler(state=UserData.check_out_day_low)
async def check_out_day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_out_day_low.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_out_day_low'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

    await UserData.check_out_date_low.set()
    await confirmation(callback.message)


@dp.callback_query_handler(state=UserData.check_out_day_high)
async def check_out_day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_out_day_high.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_out_day_high'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

    await UserData.check_out_date_high.set()
    await confirmation(callback.message)


@dp.callback_query_handler(state=UserData.check_out_day_custom)
async def check_out_day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_out_day_custom.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_out_day_custom'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

    await UserData.check_out_date_custom.set()
    await confirmation(callback.message)
