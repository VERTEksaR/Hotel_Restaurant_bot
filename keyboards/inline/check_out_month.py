from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.data import UserData
from keyboards.inline.check_out_day import select_day, day_button


month_button = InlineKeyboardMarkup()
months = [(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'),
          (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь')]


async def select_month(state: FSMContext) -> None:
    """

    Функция, создающая inline-кнопки с месяцами, указывающими когда
    можно выехать из отеля. Устанавливает состояние
    для параметра check_out_month, записывающий месяц выезда.

    :param state: (FSMContext) ссылка на машину состояний.
    :return: None

    """
    async with state.proxy() as data:
        check_in_month = int(data['check_in_month'])
        check_in_day = int(data['check_in_day'])
        if (check_in_month in [1, 3, 5, 7, 8, 10, 12]) and (check_in_day > 1):
            if check_in_month == 12:
                btn1 = InlineKeyboardButton(f'{months[11][1]}',
                                            callback_data='outmonth1')
                btn2 = InlineKeyboardButton(f'{months[0][1]}',
                                            callback_data='outmonth1.5')
            else:
                btn1 = InlineKeyboardButton(f'{months[check_in_month - 1][1]}',
                                            callback_data='outmonth1')
                btn2 = InlineKeyboardButton(f'{months[check_in_month][1]}',
                                            callback_data='outmonth2')
            month_button.add(btn1, btn2)
        elif (check_in_month in [1, 3, 5, 7, 8, 10, 12]) and (check_in_day == 1):
            btn1 = InlineKeyboardButton(f'{months[check_in_month - 1][1]}',
                                        callback_data='outmonth1')
            month_button.add(btn1)
        elif check_in_month in [2, 4, 6, 9, 11]:
            btn1 = InlineKeyboardButton(f'{months[check_in_month - 1][1]}',
                                        callback_data='outmonth1')
            btn2 = InlineKeyboardButton(f'{months[check_in_month][1]}',
                                        callback_data='outmonth2')
            month_button.add(btn1, btn2)
    await UserData.check_out_month.set()


@dp.callback_query_handler(state=UserData.check_out_month)
async def check_out_month_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """

    Функция-callback, реагирующая на изменения состояния UserData.check_out_month.
    Записывает месяц, выбранный пользователем в машину состояний, а затем
    вызывает функцию по выбору дня.

    :param callback: callback_data, передающийся от функции select_month при нажатии
    определенной кнопки;
    :param state: (FSMContext) ссылка на машину состояний.
    :return:None

    """
    if callback.data == 'outmonth1':
        async with state.proxy() as data:
            data['check_out_month'] = data['check_in_month']
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали месяц - {data["check_out_month"]}')

            await select_day(state, data['check_out_month'])
            await callback.message.answer('Выберите день:', reply_markup=day_button)

    elif callback.data == 'outmonth2':
        async with state.proxy() as data:
            check_in_month = int(data['check_in_month'])
            data['check_out_month'] = check_in_month + 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text=f'Вы выбрали месяц - {check_in_month + 1}')

        await select_day(state, data['check_out_month'])
        await callback.message.answer('Выберите день:', reply_markup=day_button)

    elif callback.data == 'outmonth1.5':
        async with state.proxy() as data:
            data['check_out_month'] = 1
            await bot.edit_message_text(chat_id=callback.message.chat.id,
                                        message_id=callback.message.message_id,
                                        text='Вы выбрали месяц - 1')

            await select_day(state, data['check_out_month'])
            await callback.message.answer('Выберите день:', reply_markup=day_button)
