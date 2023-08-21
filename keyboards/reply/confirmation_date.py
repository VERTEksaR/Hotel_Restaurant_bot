from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton


async def confirmation(message: Message) -> None:
    """

    Функция, генерирующая кнопку для подтверждения
    даты заезда.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    confirm = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Подтвердить')
    confirm.add(btn1)
    await message.answer('Для подтверждения даты нажмите "Подтвердить"',
                         reply_markup=confirm)
