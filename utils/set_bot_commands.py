from aiogram.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
