from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_num_of_hotels(message: Message) -> None:
    """

    Функция, создающая 8 reply-кнопок. Каждая из них
    обозначает то количество отелей, о которых будет
    выведена информация.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    num_hotels = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for number in range(1, 9):
        num_hotels.insert(KeyboardButton(f'{number}'))
    await UserData.number_of_hotels.set()
    await message.answer('10. Укажите количество отелей для просмотра',
                         reply_markup=num_hotels)
