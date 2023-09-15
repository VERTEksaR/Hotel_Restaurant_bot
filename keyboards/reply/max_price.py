from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_max_price(message: Message, function: str) -> None:
    """

    Функция, создающая 6 reply-кнопок: 5 из них содержат
    вариант уже написанной максимальной цены, последняя
    дает пользователю ввести свою максимальную цену.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    max_price = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    btn1 = KeyboardButton('50000')
    btn2 = KeyboardButton('60000')
    btn3 = KeyboardButton('70000')
    btn4 = KeyboardButton('80000')
    btn5 = KeyboardButton('100000')
    btn6 = KeyboardButton('Свой вариант')
    max_price.add(btn1).insert(btn2).insert(btn3).insert(btn4).insert(btn5)
    max_price.add(btn6)

    if function == 'low':
        await message.answer('9. Укажите максимальную цену поиска (руб.)',
                             reply_markup=max_price)
    elif function == 'custom':
        await message.answer('10. Укажите максимальную цену поиска (руб.)',
                             reply_markup=max_price)
