import requests
from config.settings import API_KEY


def get_forecast(city):

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return None