import requests
import random
from loguru import logger
from aiogram.types import Message, InputMediaPhoto
from aiogram.dispatcher import FSMContext

from config_data.config import RAPID_API_KEY
from utils.misc import get_restaurants, get_restaurants_info

url = "https://travel-advisor.p.rapidapi.com/restaurants/v2/list"
querystring = {"currency": "RUB", "units": "km", "lang": "ru_RU"}

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}


async def find_and_show_restaurants(message: Message, state: FSMContext, function: str) -> None:
    """

    Функция для поиска ресторанов по тем критериям, что пользователь
    ввел в машину состояний.

    :param message: (Message) сообщение, с которым работает данная функция;
    :param state: (FSMContext) ссылка на машину состояний;
    :param function: (str) функция, выбранная пользователем.
    :return: None

    """
    async with state.proxy() as data:
        if function == 'low':
            price = '10953'
            data_crit = '_low'
            sort = 'RELEVANCE'
            logger.info(f'Производится поиск ресторанов по сортировке: {sort}')
        elif function == 'high':
            price = '10954'
            data_crit = '_high'
            sort = 'RELEVANCE'
            logger.info(f'Производится поиск ресторанов по сортировке: {sort}')
        elif function == 'custom':
            price = data['restaurant_price_custom']
            data_crit = '_custom'
            sort = data['restaurant_choice_custom']
            logger.info(f'Производится поиск ресторанов по сортировке: {sort}')
            
        payload = {
            "geoId": int(data[f'geoId{data_crit}']),
            "partySize": int(data[f'group_size{data_crit}']),
            "reservationTime": f'{data[f"visiting_rest_year{data_crit}"]}-{data[f"visiting_rest_month{data_crit}"]}-'
                               f'{data[f"visiting_rest_day{data_crit}"]}T{data[f"visiting_rest_hour{data_crit}"]}:'
                               f'{data[f"visiting_rest_minute{data_crit}"]}',
            "sort": sort,
            "sortOrder": "asc",
            "filters": [
                {
                    "id": "establishment",
                    "value": ["10591"]
                },
                {
                    "id": "price",
                    "value": [price]
                }
            ],
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
        logger.info('json-объект с ресторанами получен')
        restaurants = await get_restaurants.get_restaurants(response.text)
        count = 0

        for restaurant in restaurants.values():
            if count < int(data[f'number_of_restaurants{data_crit}']):
                count += 1
                details_url = "https://travel-advisor.p.rapidapi.com/restaurants/v2/get-details"
                details_payload = {
                    "contentId": restaurant['id'],
                    "reservationTime": f'{data[f"visiting_rest_year{data_crit}"]}-'
                                       f'{data[f"visiting_rest_month{data_crit}"]}-'
                                       f'{data[f"visiting_rest_day{data_crit}"]}T'
                                       f'{data[f"visiting_rest_hour{data_crit}"]}:'
                                       f'{data[f"visiting_rest_minute{data_crit}"]}',
                    "partySize": int(data[f'group_size{data_crit}'])
                }
                detail_response = requests.post(url=details_url, json=details_payload,
                                                headers=headers, params=querystring, timeout=15)

                if detail_response.status_code == requests.codes.ok:
                    logger.info('json-объект с параметрами ресторана получен')
                    caption = await get_restaurants_info.get_restaurants_info(detail_response.text)
                    if not caption:
                        count -= 1
                    else:
                        if int(data[f'number_of_rest_photos{data_crit}']) > 0:
                            result, links = [], []
                            photos = caption[1]
                            try:
                                for photo_url in range(int(data[f'number_of_rest_photos{data_crit}'])):
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
                    logger.error('json-объект с параметрами ресторана не получен')
                    await message.answer('Не удалось подключиться к серверу')
            else:
                logger.info('Поиск завершен успешно')
                await message.answer('Поиск завершен')
                await state.finish()
                break
    else:
        logger.error('json-объект с отелями не получен')
        await message.answer('Не удалось подключиться к серверу')
