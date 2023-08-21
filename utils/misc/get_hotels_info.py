import json
from typing import Union

list_of_photos = []


async def get_hotels_info(response_text: str) -> Union[bool, tuple[str, list]]:
    """

    Функция, находящая в json-объекте название, адрес отеля, а также
    цену за проживание и фотографии.

    :param response_text: json-объект, в котором будут проходить поиски.
    :return: (str) информация об отеле: название, адрес и цена.

    """
    data = json.loads(response_text)

    common_path = data['data']['AppPresentation_queryAppDetailV2'][0]
    try:
        hotel_info = f"Название: {common_path['container']['navTitle']}\n" \
                     f"Адрес: {common_path['sections'][10]['address']['address']}\n" \
                     f"Цена: {common_path['sections'][4]['primaryOfferV2']['displayPrice']['string']}\n"
    except Exception:
        return False

    for picture in data['data']['AppPresentation_queryAppDetailV2'][0]['sections'][0]['heroContent']:
        try:
            list_of_photos.append(picture['data']['sizes'][5]['url'])
        except Exception:
            continue

    return hotel_info, list_of_photos
