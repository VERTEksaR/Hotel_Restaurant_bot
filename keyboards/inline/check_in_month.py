from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import time

from loader import dp, bot
from states.data import UserData
from keyboards.inline.check_in_day import select_day

current_year = time.localtime().tm_year
months = [(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'),
          (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')]


async def select_month(message: Message, state: FSMContext, choice: str, function: str) -> None:
    """

    Функция, создающая inline-кнопки с месяцами. Устанавливает состояние
    для параметра check_in_month, записывающий месяц посещения.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param choice: (str) выбор пользователя;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    month_button = InlineKeyboardMarkup()
    async with state.proxy() as data:
        current_month = time.localtime().tm_mon

        if choice.endswith('Отель'):
            data_state = 'check_in_year'
        elif choice.endswith('Ресторан'):
            data_state = 'visiting_rest_year'

        data_crit = f'_{function}'
        year = int(data[f'{data_state}{data_crit}'])

        if year == current_year:
            for month, name in months:
                if month >= current_month:
                    month_button.add(InlineKeyboardButton(f'{name}', callback_data=str(month)))
        else:
            for month, name in months:
                month_button.add(InlineKeyboardButton(f'{name}', callback_data=str(month)))

        await message.answer('Выберите месяц:', reply_markup=month_button)

    if choice.endswith('Отель'):
        if function == 'low':
            await UserData.check_in_month_low.set()
        elif function == 'high':
            await UserData.check_in_month_high.set()
        elif function == 'custom':
            await UserData.check_in_month_custom.set()
    elif choice.endswith('Ресторан'):
        if function == 'low':
            await UserData.visiting_rest_month_low.set()
        elif function == 'high':
            await UserData.visiting_rest_month_high.set()
        elif function == 'custom':
            await UserData.visiting_rest_month_custom.set()


@dp.callback_query_handler(state=UserData.check_in_month_low)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_month_low.
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
                choice = data['choice_low']
                data['check_in_month_low'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')
                await select_day(callback.message, state, data['check_in_month_low'], choice, 'low')


@dp.callback_query_handler(state=UserData.check_in_month_high)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_month_high.
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
                choice = data['choice_high']
                data['check_in_month_high'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')
                await select_day(callback.message, state, data['check_in_month_high'], choice, 'high')


@dp.callback_query_handler(state=UserData.check_in_month_custom)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_in_month_custom.
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
                choice = data['choice_custom']
                data['check_in_month_custom'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')
                await select_day(callback.message, state, data['check_in_month_custom'], choice, 'custom')


@dp.callback_query_handler(state=UserData.visiting_rest_month_low)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_month_low.
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
                choice = data['choice_low']
                data['visiting_rest_month_low'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')
                await select_day(callback.message, state, data['visiting_rest_month_low'], choice, 'low')


@dp.callback_query_handler(state=UserData.visiting_rest_month_high)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_month_high.
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
                choice = data['choice_high']
                data['visiting_rest_month_high'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')
                await select_day(callback.message, state, data['visiting_rest_month_high'], choice, 'high')


@dp.callback_query_handler(state=UserData.visiting_rest_month_custom)
async def month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.visiting_rest_month_custom.
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
                choice = data['choice_custom']
                data['visiting_rest_month_custom'] = number
                await bot.edit_message_text(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            text=f'Вы выбрали месяц - {callback.data}')
                await select_day(callback.message, state, data['visiting_rest_month_custom'], choice, 'custom')
