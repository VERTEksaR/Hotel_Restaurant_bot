from aiogram.types import Message

from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: Message):
    await message.reply('Эхо без состояния или фильтра.\n' f'Сообщение: {message.text}')
