from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import dp, bot
from states.data import UserData
from keyboards.reply import size_group


async def restaurant_price(message: Message) -> None:
    """

    Функция, создающая inline-кнопки с выбором сортировки цен ресторанов.

    :param message: (Message) сообщение, с которым работает данная функция;
    :return: None

    """
    price = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('$', callback_data='10953')
    btn2 = InlineKeyboardButton('$$ - $$$', callback_data='10955')
    btn3 = InlineKeyboardButton('$$$$', callback_data='10954')
    price.add(btn1).add(btn2).add(btn3)
    await UserData.restaurant_price_custom.set()
    await message.answer('6. В каком ценовом диапазоне находится ресторан?', reply_markup=price)


@dp.callback_query_handler(state=UserData.restaurant_price_custom)
async def price_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.restaurant_price_custom.
    Записывает выбор пользователя в машину состояний, а затем
    вызывает функцию по выбору размера группы.

    :param callback: callback_data, передающийся от функции restaurant_price при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    async with state.proxy() as data:
        if callback.data == '10953':
            data['restaurant_price_custom'] = 10953
            result = '$'
        elif callback.data == '10954':
            data['restaurant_price_custom'] = 10954
            result = '$$$$'
        elif callback.data == '10955':
            data['restaurant_price_custom'] = 10955
            result = '$$ - $$$'

        data['restaurant_price_symbol'] = result

    logger.info(f'Сортировать рестораны по цене: {result}')
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text=f'Вы выбрали - {result}')
    await size_group.set_group_size(callback.message, 'custom')
