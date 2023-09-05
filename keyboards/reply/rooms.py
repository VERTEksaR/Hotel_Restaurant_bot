from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_rooms(message: Message, function: str) -> None:
    """

    Функция, генерирующая 8 reply-кнопок, где каждая кнопка
    равна количеству номеров, которые пользователь может указать.
    Устанавливает состояние для параметра rooms, записывающий
    количество номеров.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    rooms = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    for room in range(1, 9):
        rooms.insert(KeyboardButton(f'{room}'))

    if function == 'low':
        await UserData.rooms_low.set()
    elif function == 'high':
        await UserData.rooms_high.set()

    await message.answer('5. Введите необходимое количество номеров',
                         reply_markup=rooms)
