from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.inline.minute_restaurant import set_minute


current_hour = time.localtime().tm_hour
current_day = time.localtime().tm_mday


async def set_hour(message: Message, state: FSMContext, day: str, function: str) -> None:
    """

    Функция, создающая inline-кнопки с часами, позволяющая
    пользователю выбрать час для бронирования ресторана.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param day: (str) день, выбранный пользователем;
    :param function: (str) функция, выбранная пользователем.
    :return:

    """
    hours_buttons = InlineKeyboardMarkup(row_width=6)
    async with state.proxy() as data:
        data_crit = f'_{function}'
        data[f'visiting_rest_day{data_crit}'] = int(day)

    if current_day == int(day):
        for hour in range(current_hour, 24):
            hours_buttons.insert(InlineKeyboardButton(f'{hour}', callback_data=str(hour)))
    else:
        for hour in range(24):
            hours_buttons.insert(InlineKeyboardButton(f'{hour}', callback_data=str(hour)))

    if function == 'low':
        await UserData.visiting_rest_hour_low.set()
    elif function == 'high':
        await UserData.visiting_rest_hour_high.set()
    elif function == 'custom':
        await UserData.visiting_rest_hour_custom.set()

    await message.answer('Выберите час:', reply_markup=hours_buttons)


@dp.callback_query_handler(state=UserData.visiting_rest_hour_low)
async def callback_hour(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_hour_low.
    Записывает час, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору минут.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(24):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['visiting_rest_hour_low'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали час - {callback.data}')

            await set_minute(callback.message, 'low')


@dp.callback_query_handler(state=UserData.visiting_rest_hour_high)
async def callback_hour(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_hour_high.
    Записывает час, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору минут.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(24):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['visiting_rest_hour_high'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали час - {callback.data}')

            await set_minute(callback.message, 'high')


@dp.callback_query_handler(state=UserData.visiting_rest_hour_custom)
async def callback_hour(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_hour_custom.
    Записывает час, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору минут.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(24):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['visiting_rest_hour_custom'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали час - {callback.data}')

            await set_minute(callback.message, 'custom')
