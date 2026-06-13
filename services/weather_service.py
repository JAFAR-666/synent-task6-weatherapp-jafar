import requests
from config.settings import API_KEY

def get_current_weather(city):

    url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={city}&appid={API_KEY}&units=metric"
)

    response = requests.get(url)

    print(response.status_code)
    print(response.text)

    if response.status_code == 200:
        return response.json()

    return None