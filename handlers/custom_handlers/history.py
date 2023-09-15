from aiogram.types import Message
from loguru import logger

from database.models import Choice, User
from loader import dp


@dp.message_handler(commands=['history'])
async def command_history(message: Message) -> None:
    """

    Функция, реагирующая на команду /history.
    Выводит последний 10 запросов того пользователя, который ввел эту команду.

    :param message: (Message) сообщение, с которым работает данная функция;
    :return: None

    """
    logger.info('Пользователь ввел команду /history')
    user_id = message.from_user.id
    needed_id, count, result = 0, 1, ''

    for user in User.select():
        if user_id == User.user_id:
            needed_id = user

    total_requests = Choice.select().count()

    sort_requests = total_requests - 10

    requests = Choice.select().where(Choice.user == needed_id).offset(sort_requests)

    if requests:
        for request in requests:
            result += f'Запрос {count}\n'
            result += f'Город: {request.city}\nКоманда: {request.command}\nВыбор: {request.choice}\n' \
                      f'Дата запроса: {request.date_of_request}\nДата посещения: {request.date_of_visit}\n' \
                      f'Сортировка по: {request.sort}\n\n'
            count += 1

        await message.answer(f'Последние 10 запросов:\n\n{result}')
    else:
        await message.answer(f'На данный момент запросов нет')
