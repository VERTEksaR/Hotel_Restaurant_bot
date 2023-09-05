from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

from states.data import UserData


async def total_adults(message: Message, state: FSMContext, rooms: str, function: str) -> None:
    """

    Функция, генерирующая reply-кнопки в количестве, зависящем
    от количества номеров. Каждая кнопка обозначает определенное
    количество взрослых персон. Устанавливает состояние для параметра adults,
    записывающий количество номеров.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param rooms: (str) количество комнат;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    async with state.proxy() as data:
        if function == 'low':
            data['rooms_low'] = rooms
            total_rooms = int(data['rooms_low'])
        elif function == 'high':
            data['rooms_high'] = rooms
            total_rooms = int(data['rooms_high'])

    adults = ReplyKeyboardMarkup(resize_keyboard=True, row_width=8)
    for adult in range(total_rooms, total_rooms * 4 + 1):
        adults.insert(KeyboardButton(f'{adult}'))

    if function == 'low':
        await UserData.adults_low.set()
    elif function == 'high':
        await UserData.adults_high.set()

    await message.answer('6. Введите количество взрослых персон',
                         reply_markup=adults)
