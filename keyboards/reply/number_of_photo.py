from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from states.data import UserData


async def set_num_of_photo(message: Message) -> None:
    """

    Функция, создающая 5 reply-кнопок. Каждая из них
    обозначает то количество фотографий, которое будет
    изображено для каждого отеля.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: None

    """
    num_photos = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for number in range(1, 6):
        num_photos.insert(KeyboardButton(f'{number}'))
    await UserData.number_of_photos.set()
    await message.answer('11. Укажите количество фотографий для просмотра',
                         reply_markup=num_photos)
