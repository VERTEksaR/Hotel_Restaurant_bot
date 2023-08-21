from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

from states.data import UserData


async def total_adults(message: Message, state: FSMContext, rooms: str) -> None:
    """

    Функция, генерирующая reply-кнопки в количестве, зависящем
    от количества номеров. Каждая кнопка обозначает определенное
    количество взрослых персон. Устанавливает состояние для параметра adults,
    записывающий количество номеров.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param rooms: (str) количество комнат.
    :return: None

    """
    async with state.proxy() as data:
        data['rooms'] = rooms
        total_rooms = int(data['rooms'])
    adults = ReplyKeyboardMarkup(resize_keyboard=True, row_width=8)
    for adult in range(1, total_rooms * 4 + 1):
        adults.insert(KeyboardButton(f'{adult}'))
    await UserData.adults.set()
    await message.answer('6. Введите количество взрослых персон',
                         reply_markup=adults)
