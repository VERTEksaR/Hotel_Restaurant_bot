from aiogram import executor

from database.models import create_models
from handlers import dp
from utils.set_bot_commands import set_default_commands


async def on_startup(_):
    print('I have been started up')

    await create_models()
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
