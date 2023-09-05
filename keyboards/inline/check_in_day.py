from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.reply.confirmation_date import confirmation
from keyboards.inline.hour_restaurant import set_hour

current_month = time.localtime().tm_mon
current_year = time.localtime().tm_year


async def filling_buttons(message: Message, day: int, total_days: int) -> None:
    """

    Функция, генерирующая inline-кнопки с днями, указывающими
    когда можно заселиться в отель.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param day: (int) текущий день или первый день месяца;
    :param total_days: (int) оставшиеся дни для выбора в месяце.
    :return: None

    """
    day_button = InlineKeyboardMarkup(row_width=7)
    for days in range(day, total_days):
        day_button.insert(InlineKeyboardButton(text=f'{days}', callback_data=str(days)))
    await message.answer('Выберите день:', reply_markup=day_button)


async def select_day(message: Message, state: FSMContext, month: str, choice: str, function: str) -> None:
    """

    Функция, задающая параметры day и total_days для функции filling_buttons().
    Устанавливает состояние для параметра check_in_day, записывающий день заезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param month: (str) месяц заезда;
    :param choice: (str) выбор пользователя;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    async with state.proxy() as data:
        if choice.endswith('Отель') and function == 'low':
            data['check_in_month_low'] = month
            year = int(data['check_in_year_low'])
        elif choice.endswith('Отель') and function == 'high':
            data['check_in_month_high'] = month
            year = int(data['check_in_year_high'])
        elif choice.endswith('Ресторан') and function == 'low':
            data['visiting_rest_month_low'] = month
            year = int(data['visiting_rest_year_low'])
        elif choice.endswith('Ресторан') and function == 'high':
            data['visiting_rest_month_high'] = month
            year = int(data['visiting_rest_year_high'])

        an_month = int(month)

        if (an_month == current_month) and (year == current_year):
            current_day = time.localtime().tm_mday
            if an_month in [1, 3, 5, 7, 8, 10, 12]:
                await filling_buttons(message, current_day, 32)

            elif an_month in [4, 6, 9, 11]:
                await filling_buttons(message, current_day, 31)

            else:
                if an_month % 4 == 0:
                    await filling_buttons(message, current_day, 30)
                else:
                    await filling_buttons(message, current_day, 29)
        else:
            if an_month in [1, 3, 5, 7, 8, 10, 12]:
                await filling_buttons(message, 1, 32)

            elif an_month in [4, 6, 9, 11]:
                await filling_buttons(message, 1, 31)

            else:
                if an_month % 4 == 0:
                    await filling_buttons(message, 1, 30)
                else:
                    await filling_buttons(message, 1, 29)

    if choice.endswith('Отель') and function == 'low':
        await UserData.check_in_day_low.set()
    elif choice.endswith('Отель') and function == 'high':
        await UserData.check_in_day_high.set()
    elif choice.endswith('Ресторан') and function == 'low':
        await UserData.visiting_rest_day_low.set()
    elif choice.endswith('Ресторан') and function == 'high':
        await UserData.visiting_rest_day_high.set()


@dp.callback_query_handler(state=UserData.check_in_day_low)
async def day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_day_low.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_in_day_low'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')
                await UserData.check_in_date_low.set()
                await confirmation(callback.message)


@dp.callback_query_handler(state=UserData.check_in_day_high)
async def day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_day_high.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['check_in_day_high'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')
                await UserData.check_in_date_high.set()
                await confirmation(callback.message)


@dp.callback_query_handler(state=UserData.visiting_rest_day_low)
async def day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_day_low.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
#                choice = data['choice_low']
                data['visiting_rest_day_low'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

#                if choice.endswith('Отель'):
#                   await UserData.check_in_date_low.set()
#                    await confirmation(callback.message)
#                elif choice.endswith('Ресторан'):
                await UserData.check_date_low.set()
                await set_hour(callback.message, state, callback.data, 'low')


@dp.callback_query_handler(state=UserData.visiting_rest_day_high)
async def day_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_day_high.
    Записывает день, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_day при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 32):
        if str(number) == callback.data:
            async with state.proxy() as data:
#                choice = data['choice_high']
                data['visiting_rest_day_high'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали день - {callback.data}')

#                if choice.endswith('Отель'):
#                   await UserData.check_in_date_low.set()
#                    await confirmation(callback.message)
#                elif choice.endswith('Ресторан'):
                await UserData.check_date_high.set()
                await set_hour(callback.message, state, callback.data, 'high')
