from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_rooms(message: Message) -> None:
    """

    Функция, генерирующая 8 reply-кнопок, где каждая кнопка
    равна количеству номеров, которые пользователь может указать.
    Устанавливает состояние для параметра rooms, записывающий
    количество номеров.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    rooms = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    for room in range(1, 9):
        rooms.insert(KeyboardButton(f'{room}'))
    await UserData.rooms.set()
    await message.answer('5. Введите необходимое количество номеров',
                         reply_markup=rooms)
