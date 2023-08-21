from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.inline.check_in_day import day_button, select_day

current_year = time.localtime().tm_year
month_button = InlineKeyboardMarkup()


async def select_month(state: FSMContext, choice: str) -> None:
    """

    Функция, создающая inline-кнопки с месяцами. Устанавливает состояние
    для параметра check_in_month, записывающий месяц посещения.

    :param state: (FSMContext) ссылка на машину состояний;
    :param choice: (str) выбор пользователя.
    :return: None

    """
    async with state.proxy() as data:
        current_month = time.localtime().tm_mon
        if choice.endswith('Отель'):
            year = int(data['check_in_year'])
        elif choice.endswith('Ресторан'):
            year = int(data['visiting_rest_year'])

        if year == current_year:
            for month in range(current_month, 13):
                month_button.add(InlineKeyboardButton(f'{month}', callback_data=str(month)))
        else:
            for month in range(1, current_month + 1):
                month_button.add(InlineKeyboardButton(f'{month}', callback_data=str(month)))

    if choice.endswith('Отель'):
        await UserData.check_in_month.set()
    elif choice.endswith('Ресторан'):
        await UserData.visiting_rest_month.set()


@dp.callback_query_handler(state=UserData.check_in_month)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_month.
    Записывает месяц, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору дня.

    :param callback: callback_data, передающийся от функции select_month при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 13):
        if str(number) == callback.data:
            async with state.proxy() as data:
                choice = data['choice']
                data['check_in_month'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')

                await select_day(state, data['check_in_month'], choice)
                await callback.message.answer('Выберите день:', reply_markup=day_button)


@dp.callback_query_handler(state=UserData.visiting_rest_month)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_month.
    Записывает месяц, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору дня.

    :param callback: callback_data, передающийся от функции select_month при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    for number in range(1, 13):
        if str(number) == callback.data:
            async with state.proxy() as data:
                choice = data['choice']
                data['visiting_rest_month'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')

                await select_day(state, data['visiting_rest_month'], choice)
                await callback.message.answer('Выберите день:', reply_markup=day_button)
