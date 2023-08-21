import json
from typing import Any


async def get_restaurants(response_text: str) -> dict[Any, dict[str, Any]]:
    """

    Функция, заполняющая словарь hotels_data названиями ресторанов и
    их id, которые удовлетворяют условиям пользователя.

    :param response_text: json-объект, в котором будут проходить поиски.
    :return: (dict[Any, dict[str, Any]]:) словарь с названиями отелей и их id.

    """
    data = json.loads(response_text)

    restaurants_data = {}

    for position in data['data']['AppPresentation_queryAppListV2'][0]['sections']:
        try:
            restaurants_data[position['listSingleCardContent']['saveId']['id']] = {
                'name': position['listSingleCardContent']['cardTitle']['string'],
                'id': position['listSingleCardContent']['saveId']['id']
            }
        except Exception:
            continue

    return restaurants_data


