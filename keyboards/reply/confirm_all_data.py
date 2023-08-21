from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def confirmation(message: Message) -> None:
    """

    Функция, генерирующая кнопку для подтверждения, что все
    данные введены.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    confirm = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton('Подтвердить')
    confirm.add(btn1)
    await message.answer('Для подтверждения указанных данных нажмите "Подтвердить"',
                         reply_markup=confirm)
