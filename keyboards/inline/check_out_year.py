from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.data import UserData
from keyboards.inline.check_out_month import select_month


async def select_year(message: Message, state: FSMContext, function: str) -> None:
    """

    Функция, создающая inline-кнопки с годами, указывающими когда
    можно выехать из отеля. Устанавливает состояние
    для параметра check_out_year, записывающий год выезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    year_button = InlineKeyboardMarkup()
    async with state.proxy() as data:
        data_crit = f'_{function}'
        check_in_day = int(data[f'check_in_day{data_crit}'])
        check_in_month = int(data[f'check_in_month{data_crit}'])
        check_in_year = int(data[f'check_in_year{data_crit}'])

        if check_in_month < 12:
            btn1 = InlineKeyboardButton(f'{check_in_year}',
                                        callback_data='outbtn1')
            year_button.add(btn1)
        elif (check_in_month == 12) and (check_in_day == 1):
            btn1 = InlineKeyboardButton(f'{check_in_year}',
                                        callback_data='outbtn1')
            year_button.add(btn1)
        elif (check_in_month == 12) and (check_in_day > 1):
            btn1 = InlineKeyboardButton(f'{check_in_year}',
                                        callback_data='outbtn1')
            btn2 = InlineKeyboardButton(f'{check_in_year + 1}',
                                        callback_data='outbtn2')
            year_button.add(btn1, btn2)

        if function == 'low':
            await UserData.check_out_year_low.set()
        elif function == 'high':
            await UserData.check_out_year_high.set()
        elif function == 'custom':
            await UserData.check_out_year_custom.set()

        await message.answer('Выберите год:', reply_markup=year_button)


@dp.callback_query_handler(state=UserData.check_out_year_low)
async def check_out_year_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.check_out_year_low.
    Записывает год, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору месяца.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    if callback.data == 'outbtn1':
        async with state.proxy() as data:
            check_in_year = data['check_in_year_low']
            data['check_out_year_low'] = check_in_year
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year}')
            await select_month(callback.message, state, 'low')

    elif callback.data == 'outbtn2':
        async with state.proxy() as data:
            check_in_year = data['check_in_year_low']
            data['check_out_year_low'] = check_in_year + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year + 1}')
            await select_month(callback.message, state, 'low')


@dp.callback_query_handler(state=UserData.check_out_year_high)
async def check_out_year_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.check_out_year_high.
    Записывает год, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору месяца.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    if callback.data == 'outbtn1':
        async with state.proxy() as data:
            check_in_year = data['check_in_year_high']
            data['check_out_year_high'] = check_in_year
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year}')
            await select_month(callback.message, state, 'high')

    elif callback.data == 'outbtn2':
        async with state.proxy() as data:
            check_in_year = data['check_in_year_high']
            data['check_out_year_high'] = check_in_year + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year + 1}')
            await select_month(callback.message, state, 'high')


@dp.callback_query_handler(state=UserData.check_out_year_custom)
async def check_out_year_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.check_out_year_custom.
    Записывает год, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору месяца.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    if callback.data == 'outbtn1':
        async with state.proxy() as data:
            check_in_year = data['check_in_year_custom']
            data['check_out_year_custom'] = check_in_year
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year}')
            await select_month(callback.message, state, 'custom')

    elif callback.data == 'outbtn2':
        async with state.proxy() as data:
            check_in_year = data['check_in_year_custom']
            data['check_out_year_custom'] = check_in_year + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year + 1}')
            await select_month(callback.message, state, 'custom')
