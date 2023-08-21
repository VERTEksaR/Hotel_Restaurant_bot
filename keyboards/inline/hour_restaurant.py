from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.inline.minute_restaurant import minute_buttons, set_minute


current_hour = time.localtime().tm_hour
current_day = time.localtime().tm_mday
hours_buttons = InlineKeyboardMarkup(row_width=6)


async def set_hour(state: FSMContext, day: str) -> None:
    """

    Функция, создающая inline-кнопки с часами, позволяющая
    пользователю выбрать час для бронирования ресторана.

    :param state: (FSMContext) ссылка на машину состояний;
    :param day: (str) день, выбранный пользователем.
    :return:

    """
    async with state.proxy() as data:
        data['visiting_rest_day'] = int(day)

    if current_day == int(day):
        for hour in range(current_hour, 24):
            hours_buttons.insert(InlineKeyboardButton(f'{hour}', callback_data=str(hour)))
    else:
        for hour in range(24):
            hours_buttons.insert(InlineKeyboardButton(f'{hour}', callback_data=str(hour)))

    await UserData.visiting_rest_hour.set()


@dp.callback_query_handler(state=UserData.visiting_rest_hour)
async def callback_hour(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_hour.
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
                data['visiting_rest_hour'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали час - {callback.data}')

            await set_minute(state)
            await callback.message.answer('Выберите минуты:', reply_markup=minute_buttons)
