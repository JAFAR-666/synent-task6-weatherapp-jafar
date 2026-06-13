import requests
from config.settings import API_KEY


def get_aqi(lat, lon):

    url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None