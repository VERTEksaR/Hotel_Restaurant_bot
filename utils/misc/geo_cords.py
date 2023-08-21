from geopy.geocoders import Nominatim
from aiogram.dispatcher import FSMContext


async def set_geo_cords(state: FSMContext) -> None:
    """

    Функция, определяющая широту и долготу города.

    :param state: (FSMContext) ссылка на машину состояний.
    :return: False

    """
    async with state.proxy() as data:
        geolocator = Nominatim(user_agent='TeleBot')
        address_city = data['name_of_city']
        location_city = geolocator.geocode(address_city)
        data['latitude'] = location_city.latitude
        data['longitude'] = location_city.longitude
