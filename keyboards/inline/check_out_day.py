from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.data import UserData
from keyboards.reply.confirmation_date import confirmation

day_button = InlineKeyboardMarkup(row_width=7)


def filling_buttons(day: int, total_days: int) -> None:
    """

    Функция, генерирующая inline-кнопки с днями, указывающими
    когда можно выехать из отеля.

    :param day: (int) день заселения или первый день месяца;
    :param total_days: (int) оставшиеся дни для выбора в месяце.
    :return: None

    """
    for days in range(day, total_days):
        day_button.insert(InlineKeyboardButton(text=f'{days}', callback_data=str(days)))


async def select_day(state: FSMContext, month: str) -> None:
    """

    Функция, задающая параметры day и total_days для функции filling_buttons().
    Устанавливает состояние для параметра check_out_day, записывающий день выезда.

    :param state: (FSMContext) ссылка на машину состояний;
    :param month: (str) месяц выезда.
    :return: None

    """
    async with state.proxy() as data:
        check_in_year = int(data['check_in_year'])
        check_in_month = int(data['check_in_month'])
        check_in_day = int(data['check_in_day'])
        check_out_month = int(month)
        if check_out_month == check_in_month:
            if check_out_month in [1, 3, 5, 7, 8, 10, 12]:
                filling_buttons(check_in_day + 1, 32)
            elif check_out_month in [4, 6, 9, 11]:
                filling_buttons(check_in_day + 1, 31)
            elif (check_out_month == 2) and (check_in_year % 4 == 0):
                filling_buttons(check_in_day + 1, 30)
            elif (check_out_month == 2) and (check_in_year % 4 != 0):
                filling_buttons(check_in_day + 1, 29)
        else:
            if check_out_month in [1, 3, 5, 7, 8, 10, 12]:
                filling_buttons(1, check_in_day + 1)
            elif check_out_month in [4, 6, 9, 11]:
                filling_buttons(1, check_in_day)
            elif (check_out_month == 2) and (check_in_year % 4 == 0):
                filling_buttons(1, check_in_day)
            elif (check_out_month == 2) and (check_in_year % 4 != 0):
                filling_buttons(1, check_in_day + 1)

    await UserData.check_out_day.set()


@dp.callback_query_handler(state=UserData.check_out_day)
async def check_out_day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_out_day.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_out_day'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

    await UserData.check_out_date.set()
    await confirmation(callback.message)


