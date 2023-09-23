from aiogram.types import Message


async def name_of_city(message: Message) -> str:
    """

    Функция, переводящая первые буквы названия городов в верхний регистр.

    :param message: (Message) сообщение, с которым работает данная функция.
    :return: (str) обработанное название города.

    """
    symbol = [' ', '-']
    result = message.text.capitalize()

    for symb in symbol:
        element = symb
        if symb in message.text:
            names = message.text.split(symb)
            new_city_name = [name.capitalize() for name in names]
            result = f'{element}'.join(new_city_name)

    return result
