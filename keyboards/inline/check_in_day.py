from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time
import loguru

from loader import dp, bot
from states.data import UserData
from keyboards.reply.confirmation_date import confirmation
from keyboards.inline.hour_restaurant import hours_buttons, set_hour

current_month = time.localtime().tm_mon
current_year = time.localtime().tm_year
day_button = InlineKeyboardMarkup(row_width=7)


async def filling_buttons(day: int, total_days: int) -> None:
    """

    Функция, генерирующая inline-кнопки с днями, указывающими
    когда можно заселиться в отель.

    :param day: (int) текущий день или первый день месяца;
    :param total_days: (int) оставшиеся дни для выбора в месяце.
    :return: None

    """
    for days in range(day, total_days):
        day_button.insert(InlineKeyboardButton(text=f'{days}', callback_data=str(days)))


async def select_day(state: FSMContext, month: str, choice: str) -> None:
    """

    Функция, задающая параметры day и total_days для функции filling_buttons().
    Устанавливает состояние для параметра check_in_day, записывающий день заезда.

    :param state: (FSMContext) ссылка на машину состояний;
    :param month: (str) месяц заезда;
    :param choice: (str) выбор пользователя.
    :return: None

    """
    async with state.proxy() as data:
        data['check_in_month'] = month

        if choice.endswith('Отель'):
            an_month = int(month)
        elif choice.endswith('Ресторан'):
            an_month = int(month)

        if (an_month == current_month) and (int(data['check_in_year']) == current_year):
            current_day = time.localtime().tm_mday
            if an_month in [1, 3, 5, 7, 8, 10, 12]:
                await filling_buttons(current_day, 32)

            elif an_month in [4, 6, 9, 11]:
                await filling_buttons(current_day, 31)

            else:
                if an_month % 4 == 0:
                    await filling_buttons(current_day, 30)
                else:
                    await filling_buttons(current_day, 29)
        else:
            if an_month in [1, 3, 5, 7, 8, 10, 12]:
                await filling_buttons(1, 32)

            elif an_month in [4, 6, 9, 11]:
                await filling_buttons(1, 31)

            else:
                if an_month % 4 == 0:
                    await filling_buttons(1, 30)
                else:
                    await filling_buttons(1, 29)

    if choice.endswith('Отель'):
        await UserData.check_in_day.set()
    elif choice.endswith('Ресторан'):
        await UserData.visiting_rest_day.set()


@dp.callback_query_handler(state=UserData.check_in_day)
async def day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_day.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_in_day'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')
                await UserData.check_in_date.set()
                await confirmation(callback.message)


@dp.callback_query_handler(state=UserData.visiting_rest_day)
async def day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_day.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                choice = data['choice']
                data['visiting_rest_day'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

                if choice.endswith('Отель'):
                    await UserData.check_in_date.set()
                    await confirmation(callback.message)
                elif choice.endswith('Ресторан'):
                    await UserData.check_date.set()
                    await set_hour(state, callback.data)
                    await callback.message.answer('Выберите час:', reply_markup=hours_buttons)
