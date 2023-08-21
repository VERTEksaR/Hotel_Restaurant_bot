from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.inline.check_in_month import month_button, select_month

current_year = time.localtime().tm_year


async def select_year(message: Message, choice: str) -> None:
    """

    Функция, создающая inline-кнопки с годами. Устанавливает состояние
    для параметра check_in_year, записывающий год посещения.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param choice: (str) выбор пользователя.
    :return: None

    """
    year_button = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(f'{current_year}',
                                callback_data='btn1')
    btn2 = InlineKeyboardButton(f'{current_year + 1}',
                                callback_data='btn2')
    year_button.add(btn1, btn2)

    if choice.endswith('Отель'):
        await UserData.check_in_year.set()
    elif choice.endswith('Ресторан'):
        await UserData.visiting_rest_year.set()
    await message.answer('Выберите год:', reply_markup=year_button)


@dp.callback_query_handler(state=UserData.check_in_year)
async def year_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_year.
    Записывает год, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору месяца.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    global current_year
    if callback.data == 'btn1':
        async with state.proxy() as data:
            choice = data['choice']
            data['check_in_year'] = current_year
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {current_year}')
        await select_month(state, choice)
        await callback.message.answer('Выберите месяц:', reply_markup=month_button)

    elif callback.data == 'btn2':
        async with state.proxy() as data:
            choice = data['choice']
            data['check_in_year'] = current_year + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {current_year + 1}')
        await select_month(state, choice)
        await callback.message.answer('Выберите месяц:', reply_markup=month_button)


@dp.callback_query_handler(state=UserData.visiting_rest_year)
async def year_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_year.
    Записывает год, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору месяца.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    global current_year
    if callback.data == 'btn1':
        async with state.proxy() as data:
            choice = data['choice']
            data['visiting_rest_year'] = current_year
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {current_year}')
        await select_month(state, choice)
        await callback.message.answer('Выберите месяц:', reply_markup=month_button)

    elif callback.data == 'btn2':
        async with state.proxy() as data:
            choice = data['choice']
            data['visiting_rest_year'] = current_year + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {current_year + 1}')
        await select_month(state, choice)
        await callback.message.answer('Выберите месяц:', reply_markup=month_button)
