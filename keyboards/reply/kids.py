from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext

from states.data import UserData


async def total_kids(message: Message, state: FSMContext, function: str) -> None:
    """

    Функция, генерирующая reply-кнопки в количестве, зависящем
    от количества взрослых персон. Каждая кнопка обозначает определенное
    количество детей. Устанавливает состояние для параметра kids,
    записывающий количество детей.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    async with state.proxy() as data:
        data_crit = f'_{function}'
        adults = int(data[f'adults{data_crit}'])

    kids = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
    if adults < 5:
        for child in range(11):
            kids.insert(KeyboardButton(f'{child}'))
    else:
        for child in range(21):
            kids.insert(KeyboardButton(f'{child}'))

    if function != 'custom':
        if function == 'low':
            await UserData.kids_low.set()
        elif function == 'high':
            await UserData.kids_high.set()

        await message.answer('7. Введите количество детей',
                             reply_markup=kids)
    elif function == 'custom':
        await UserData.kids_custom.set()
        await message.answer('8. Введите количество детей',
                             reply_markup=kids)
