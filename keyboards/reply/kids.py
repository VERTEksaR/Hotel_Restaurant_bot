from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

from states.data import UserData


async def total_kids(message: Message, state: FSMContext) -> None:
    """

    Функция, генерирующая reply-кнопки в количестве, зависящем
    от количества взрослых персон. Каждая кнопка обозначает определенное
    количество детей. Устанавливает состояние для параметра kids,
    записывающий количество детей.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    async with state.proxy() as data:
        adults = int(data['adults'])
    kids = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
    if adults < 5:
        for child in range(11):
            kids.insert(KeyboardButton(f'{child}'))
    else:
        for child in range(21):
            kids.insert(KeyboardButton(f'{child}'))
    await UserData.kids.set()
    await message.answer('7. Введите количество детей',
                         reply_markup=kids)
