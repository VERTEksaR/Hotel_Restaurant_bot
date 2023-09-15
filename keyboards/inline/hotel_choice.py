from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp, bot
from states.data import UserData
from keyboards.reply import rooms


async def hotel_choice(message: Message) -> None:
    """

    Функция, создающая inline-кнопки с выбором сортировки отелей.

    :param message: (Message) сообщение, с которым работает данная функция;
    :return: None

    """
    hotel = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Лучшая цена', callback_data='better_price')
    btn2 = InlineKeyboardButton('Расстояние от центра города', callback_data='distance')
    btn3 = InlineKeyboardButton('Цена: от минимальной до максимальной', callback_data='low_to_high')
    btn4 = InlineKeyboardButton('Популярность', callback_data='popularity')
    hotel.add(btn1).add(btn2).add(btn3).add(btn4)
    await UserData.hotel_choice_custom.set()
    await message.answer('5. По какому критерию будет проходить сортировка отелей?', reply_markup=hotel)


@dp.callback_query_handler(state=UserData.hotel_choice_custom)
async def hotel_choice_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.hotel_choice_custom.
    Записывает выбор пользователя в машину состояний, а затем
    вызывает функцию по выбору количества номеров.

    :param callback: callback_data, передающийся от функции hotel_choice при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    async with state.proxy() as data:
        if callback.data == 'better_price':
            data['hotel_choice_custom'] = 'BEST_VALUE'
            result = 'Лучшая цена'
        elif callback.data == 'distance':
            data['hotel_choice_custom'] = 'DISTANCE_FROM_CITY_CENTER'
            result = 'Расстояние от центра города'
        elif callback.data == 'low_to_high':
            data['hotel_choice_custom'] = 'PRICE_LOW_TO_HIGH'
            result = 'Цена: от минимальной до максимальной'
        elif callback.data == 'popularity':
            data['hotel_choice_custom'] = 'POPULARITY'
            result = 'Популярность'

        data['hotel_choice_custom_in_russian'] = result

    logger.info(f'Сортировать отели по: {result}')
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f'Вы выбрали - {result}')
    await rooms.set_rooms(callback.message, 'custom')
