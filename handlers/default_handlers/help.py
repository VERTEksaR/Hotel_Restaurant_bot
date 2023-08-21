from aiogram.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import dp


@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    await message.reply('\n'.join(text))
