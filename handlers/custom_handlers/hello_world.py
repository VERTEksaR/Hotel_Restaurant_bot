from aiogram.types import Message

from loader import dp


@dp.message_handler(commands=['hello_world'])
@dp.message_handler(lambda message: message.text.lower() == 'привет')
async def hello_world_command(message: Message):
    await message.answer('Привет, мир!')
