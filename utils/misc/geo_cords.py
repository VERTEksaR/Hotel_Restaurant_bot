from geopy.geocoders import Nominatim
from aiogram.dispatcher import FSMContext


async def set_geo_cords(state: FSMContext, function: str) -> None:
    """

    Функция, определяющая широту и долготу города.

    :param state: (FSMContext) ссылка на машину состояний;
    :param function: (str) функция, выбранная пользователем.
    :return: False

    """
    async with state.proxy() as data:
        geolocator = Nominatim(user_agent='TeleBot')

        if function == 'low':
            address_city = data['name_of_city_low']
        elif function == 'high':
            address_city = data['name_of_city_high']
        elif function == 'custom':
            address_city = data['name_of_city_custom']

        location_city = geolocator.geocode(address_city)
        data['latitude'] = location_city.latitude
        data['longitude'] = location_city.longitude
