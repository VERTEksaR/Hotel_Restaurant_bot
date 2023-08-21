import json
from typing import Union

list_of_photos = []


async def get_restaurants_info(response_text: str) -> Union[bool, tuple[str, list]]:
    """

    Функция, находящая в json-объекте название, адрес ресторана, а также
    его описание и фотографии.

    :param response_text: json-объект, в котором будут проходить поиски.
    :return: (str) информация о ресторане: название, адрес и описание.

    """
    data = json.loads(response_text)

    try:
        common_path = data['data']['AppPresentation_queryAppDetailV2'][0]
        restaurant_info = f'Название: {common_path["container"]["navTitle"]}\n' \
                          f'Адрес: {common_path["sections"][10]["address"]["address"]}\n' \
                          f'Описание: {common_path["sections"][2]["tagsV2"]["text"]}'
    except Exception:
        return False

    for _ in data['data']['AppPresentation_queryAppDetailV2'][0]['sections']:
        if 'heroContent' in data['data']['AppPresentation_queryAppDetailV2'][0]['sections'][0]:
            for picture in data['data']['AppPresentation_queryAppDetailV2'][0]['sections'][0]['heroContent']:
                try:
                    list_of_photos.append(picture['data']['sizes'][5]['url'])
                except Exception:
                    continue

    return restaurant_info, list_of_photos
