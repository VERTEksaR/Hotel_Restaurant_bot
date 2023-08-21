from typing import List, Union

from aiogram.dispatcher import FSMContext


async def distribution_people(state: FSMContext) -> List[dict[str, Union[int, list]]]:
    """

    Функция, распределяющая людей по отдельным номерам. Возвращает
    список, состоящий из комнат, в каждой из которых указано
    количество взрослых людей и возраст детей (если детей 0,
    то список возрастов остается пустым).

    :param state: (FSMContext) ссылка на машину состояний.
    :return: List[dict[str, Union[int, list]]]

    """
    rooms = []
    people = {
        'adults': 0,
        'childrenAges': []
    }

    async with state.proxy() as data:
        total_adults = int(data['adults'])
        total_kids = int(data['kids'])
        total_rooms = int(data['rooms'])
    int_number_of_adults = total_adults // total_rooms
    non_int_number_of_adults = total_adults % total_rooms
    int_number_of_kids = total_kids // total_rooms
    non_int_number_of_kids = total_kids % total_rooms

    for room in range(total_rooms):
        for _ in range(int_number_of_adults):
            people['adults'] += 1
        for _ in range(int_number_of_kids):
            people['childrenAges'].append(2)
        rooms.append(people.copy())
        people = {
            'adults': 0,
            'childrenAges': []
        }

    for adult in range(non_int_number_of_adults):
        rooms[adult]['adults'] += 1

    for kid in range(non_int_number_of_kids):
        rooms[kid]['childrenAges'].append(2)

    return rooms
