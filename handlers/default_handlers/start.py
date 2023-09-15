from aiogram.types import Message
from peewee import IntegrityError

from database.models import User, db
from loader import dp


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    try:
        with db:
            user = User.get_or_none(User.user_id == message.from_user.id)

            if user is None:
                User.create(user_id=user_id, username=username, first_name=first_name)

        await message.answer(f'Привет, {message.from_user.first_name}!')
    except IntegrityError:
        await message.answer(f'Привет, {message.from_user.first_name}!')
