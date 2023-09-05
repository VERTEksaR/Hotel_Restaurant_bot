from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_num_of_photo(message: Message, function: str) -> None:
    """

    Функция, создающая 5 reply-кнопок. Каждая из них
    обозначает то количество фотографий, которое будет
    изображено для каждого ресторана.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    num_photos = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for number in range(1, 6):
        num_photos.insert(KeyboardButton(f'{number}'))

    if function == 'low':
        await UserData.number_of_rest_photos_low.set()
    elif function == 'high':
        await UserData.number_of_rest_photos_high.set()

    await message.answer('6. Укажите количество фотографий для просмотра',
                         reply_markup=num_photos)
