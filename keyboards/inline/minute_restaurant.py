from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.reply.confirmation_date import confirmation

current_minute = time.localtime().tm_min
current_hour = time.localtime().tm_hour
current_day = time.localtime().tm_mday
minute_buttons = InlineKeyboardMarkup(row_width=2)


async def set_minute() -> None:
    """

    Функция, создающая 2 inline-кнопки с минутами, позволяющая
    пользователю выбрать минуты для бронирования ресторана.

    :return: None

    """
    minute_buttons.insert(InlineKeyboardButton('00', callback_data=str(00)))
    minute_buttons.insert(InlineKeyboardButton('30', callback_data=str(30)))
    await UserData.visiting_rest_minute.set()


@dp.callback_query_handler(state=UserData.visiting_rest_minute)
async def callback_minute(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_minute.
    Записывает час, выбранный пользователем в машину состояний.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(0, 60, 10):
        if str(number) == callback.data:
            async with state.proxy() as data:
                data['visiting_rest_minute'] = callback.data
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали - {callback.data} минут')

            await UserData.check_date.set()
            await confirmation(callback.message)
