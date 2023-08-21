from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def leisure(message: Message) -> None:
    """

    Функция, генерирующая 2 reply-кнопки, указывающие
    пользователю варианты, где провести досуг: в отеле или
    ресторане. Устанавливает состояние дял параметра choice,
    записывающий выбор пользователя.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    choice = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('🏨 Отель')
    btn2 = KeyboardButton('🍽️ Ресторан')
    choice.add(btn1, btn2)
    await UserData.choice.set()
    await message.answer('2. Вы ищете Отель или Ресторан',
                         reply_markup=choice)
