from typing import Union

import requests
import json

from config_data.config import RAPID_API_KEY


url = "https://travel-advisor.p.rapidapi.com/locations/v2/auto-complete"

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}


async def get_city_id(city_name: str) -> Union[bool, int]:
    """

    Функция, обращающаяся к сайту и проверяющая наличие id города,
    введенного пользователем в json-объекте. При наличии возвращает его,
    в обратном случае возвращает False.

    :param city_name: (str) название города;
    :return: False - если id города в json-объекте найдено не было, в
    противном случае его id (int).

    """
    querystring = {'query': city_name, 'lang': 'ru_RU', 'units': 'km'}
    response = requests.get(url=url, headers=headers, params=querystring)

    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)
        common_path = data['data']['Typeahead_autocomplete']['results']
        count = 0

        while True:
            try:
                if 'buCategory' in data['data']['Typeahead_autocomplete']['results'][count]:
                    count += 1
                else:
                    if common_path[count]['detailsV2']['names']['name'] == city_name:
                        return common_path[count]['detailsV2']['locationId']
                    else:
                        count += 1
            except Exception:
                return False
    else:
        return False
