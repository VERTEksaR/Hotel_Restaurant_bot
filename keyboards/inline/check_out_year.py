from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.data import UserData
from keyboards.inline.check_out_month import month_button, select_month

year_button = InlineKeyboardMarkup()


async def select_year(message: Message, state: FSMContext) -> None:
    """

    Функция, создающая inline-кнопки с годами, указывающими когда
    можно выехать из отеля. Устанавливает состояние
    для параметра check_out_year, записывающий год выезда.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    async with state.proxy() as data:
        check_in_month = int(data['check_in_month'])
        check_in_day = int(data['check_in_day'])
        check_in_year = int(data['check_in_year'])

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

        await UserData.check_out_year.set()
        await message.answer('Выберите год:', reply_markup=year_button)


@dp.callback_query_handler(state=UserData.check_out_year)
async def check_out_year_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция-callback, реагирующая на изменения состояния UserData.check_out_year.
    Записывает год, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору месяца.

    :param callback: callback_data, передающийся от функции select_year при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    if callback.data == 'outbtn1':
        async with state.proxy() as data:
            check_in_year = data['check_in_year']
            data['check_out_year'] = check_in_year
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year}')
            await select_month(state)
            await callback.message.answer('Выберите месяц:', reply_markup=month_button)

    elif callback.data == 'outbtn2':
        async with state.proxy() as data:
            check_in_year = data['check_in_year']
            data['check_out_year'] = check_in_year + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали год - {check_in_year + 1}')
            await select_month(state)
            await callback.message.answer('Выберите месяц:', reply_markup=month_button)
