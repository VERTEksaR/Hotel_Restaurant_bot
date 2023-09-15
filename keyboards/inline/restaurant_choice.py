from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp, bot
from states.data import UserData
from keyboards.inline import price_restaurant


async def restaurant_choice(message: Message) -> None:
    """

    Функция, создающая inline-кнопки с выбором сортировки ресторанов.

    :param message: (Message) сообщение, с которым работает данная функция;
    :return: None

    """
    restaurant = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Релевантность', callback_data='relevance')
    btn2 = InlineKeyboardButton('Популярность', callback_data='popularity')
    restaurant.add(btn1).add(btn2)
    await UserData.restaurant_choice_custom.set()
    await message.answer('5. По какому критерию будет проходить сортировка ресторанов?', reply_markup=restaurant)


@dp.callback_query_handler(state=UserData.restaurant_choice_custom)
async def restaurant_choice_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.restaurant_choice_custom.
    Записывает выбор пользователя в машину состояний, а затем
    вызывает функцию по сортировке цен ресторанов.

    :param callback: callback_data, передающийся от функции restaurant_choice при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    async with state.proxy() as data:
        if callback.data == 'relevance':
            data['restaurant_choice_custom'] = 'RELEVANCE'
            result = 'Релевантность'
        elif callback.data == 'popularity':
            data['restaurant_choice_custom'] = 'POPULARITY'
            result = 'Популярность'

        data['restaurant_choice_custom_in_russian'] = result

    logger.info(f'Сортировать рестораны по: {result}')
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f'Вы выбрали - {result}')
    await price_restaurant.restaurant_price(callback.message)
