import requests
import random
from loguru import logger
from aiogram.types import Message, InputMediaPhoto
from aiogram.dispatcher import FSMContext

from config_data.config import RAPID_API_KEY
from utils.misc import distribution_people, get_hotels, get_hotels_info


url = "https://travel-advisor.p.rapidapi.com/hotels/v2/list"
querystring = {"currency": "RUB", "units": "km", "lang": "ru_RU"}

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}


async def find_and_show_hotels(message: Message, state: FSMContext, function: str) -> None:
    """

    Функция для поиска отелей по тем критериям, что пользователь
    ввел в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    rooms_with_people = await distribution_people.distribution_people(state, function)

    async with state.proxy() as data:
        if function == 'low':
            sort = 'PRICE_LOW_TO_HIGH'
            data_crit = '_low'
            logger.info('Производится поиск отелей по сортировке: от мин. к макс. цене')
        elif function == 'high':
            sort = 'POPULARITY'
            data_crit = '_high'
            logger.info('Производится поиск отелей по сортировке: популярность')
        payload = {
            "geoId": int(data[f'geoId{data_crit}']),
            "checkIn": f'{data[f"check_in_year{data_crit}"]}-{data[f"check_in_month{data_crit}"]}-'
                       f'{data[f"check_in_day{data_crit}"]}',
            "checkOut": f'{data[f"check_out_year{data_crit}"]}-{data[f"check_out_month{data_crit}"]}-'
                        f'{data[f"check_out_day{data_crit}"]}',
            "sort": sort,
            "sortOrder": "asc",
            "filters": [
                {
                    "id": "deals",
                    "value": ["1", "2", "3"]
                },
                {
                    "id": "price",
                    "value": [data[f'min_price{data_crit}'], data[f'max_price{data_crit}']]
                },
                {
                    "id": "type",
                    "value": ["9189", "9201"]
                },
                {
                    "id": "amenity",
                    "value": ["9156", "9658", "21778", "9176"]
                },
                {
                    "id": "distFrom",
                    "value": ["2227712", "25.0"]
                },
                {
                    "id": "rating",
                    "value": ["40"]
                },
                {
                    "id": "class",
                    "value": ["9572"]
                }
            ],
            "rooms": rooms_with_people,
            "boundingBox": {
                "northEastCorner": {
                    "latitude": float(data['latitude']) + 0.13,
                    "longitude": float(data['longitude']) + 0.13
                },
                "southWestCorner": {
                    "latitude": float(data['latitude']) - 0.13,
                    "longitude": float(data['longitude']) - 0.13
                }
            },
            "updateToken": ""
        }

    response = requests.post(url=url, json=payload, headers=headers, params=querystring, timeout=15)

    if response.status_code == requests.codes.ok:
        logger.info('json-объект с отелями получен')
        hotels = await get_hotels.get_hotels(response.text)
        count = 0

        for hotel in hotels.values():
            if count < int(data[f'number_of_hotels{data_crit}']):
                count += 1
                details_url = "https://travel-advisor.p.rapidapi.com/hotels/v2/get-details"
                details_payload = {
                    "contentId": hotel['id'],
                    "checkIn": f'{data[f"check_in_year{data_crit}"]}-{data[f"check_in_month{data_crit}"]}-'
                               f'{data[f"check_in_day{data_crit}"]}',
                    "checkOut": f'{data[f"check_out_year{data_crit}"]}-{data[f"check_out_month{data_crit}"]}-'
                                f'{data[f"check_out_day{data_crit}"]}',
                    "rooms": rooms_with_people
                }
                detail_response = requests.post(url=details_url, json=details_payload,
                                                headers=headers, params=querystring, timeout=15)

                if detail_response.status_code == requests.codes.ok:
                    logger.info('json-объект с параметрами отеля получен')
                    caption = await get_hotels_info.get_hotels_info(detail_response.text)
                    if not caption:
                        count -= 1
                    else:
                        if int(data[f'number_of_photos{data_crit}']) > 0:
                            result, links = [], []
                            photos = caption[1]
                            try:
                                for photo_url in range(int(data[f'number_of_photos{data_crit}'])):
                                    links.append(photos[random.randint(0, len(photos) - 1)])
                            except Exception:
                                continue

                            for image, image_url in enumerate(links):
                                if image == 0:
                                    result.append(InputMediaPhoto(media=image_url, caption=caption[0]))
                                else:
                                    result.append(InputMediaPhoto(media=image_url))

                            await message.answer_media_group(result)
                        else:
                            await message.answer(caption[0])
                else:
                    logger.error('json-объект с параметрами отеля не получен')
                    await message.answer('Не удалось подключиться к серверу')
            else:
                logger.info('Поиск завершен успешно')
                await message.answer('Поиск завершен')
                await state.finish()
                break
    else:
        logger.error('json-объект с отелями не получен')
        await message.answer('Не удалось подключиться к серверу')
