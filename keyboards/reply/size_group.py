from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_group_size(message: Message, function: str) -> None:
    """

    Функция, генерирующая 20 reply-кнопок, где каждая обозначает
    то количество людей, сколько будет в группе.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    group = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7, one_time_keyboard=True)
    for human in range(1, 20):
        group.insert(KeyboardButton(f'{human}'))

    if function == 'low':
        await UserData.group_size_low.set()
    elif function == 'high':
        await UserData.group_size_high.set()

    await message.answer('4. Укажите размер группы', reply_markup=group)
