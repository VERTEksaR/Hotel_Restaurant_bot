from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_min_price(message: Message) -> None:
    """

    Функция, создающая 6 reply-кнопок: 5 из них содержат
    вариант уже написанной минимальной цены, последняя
    дает пользователю ввести свою минимальную цену.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    min_price = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    btn1 = KeyboardButton('0')
    btn2 = KeyboardButton('5000')
    btn3 = KeyboardButton('10000')
    btn4 = KeyboardButton('15000')
    btn5 = KeyboardButton('20000')
    btn6 = KeyboardButton('Свой вариант')
    min_price.add(btn1).insert(btn2).insert(btn3).insert(btn4).insert(btn5)
    min_price.add(btn6)
    await UserData.min_price.set()
    await message.answer('8. Укажите минимальную цену поиска (руб.)',
                         reply_markup=min_price)
