from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_num_of_rests(message: Message) -> None:
    """

    Функция, создающая 8 reply-кнопок. Каждая из них
    обозначает то количество ресторанов, о которых будет
    выведена информация.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    num_restaurants = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for number in range(1, 9):
        num_restaurants.insert(KeyboardButton(f'{number}'))
    await UserData.number_of_restaurants.set()
    await message.answer('5. Укажите количество ресторанов для просмотра',
                         reply_markup=num_restaurants)
