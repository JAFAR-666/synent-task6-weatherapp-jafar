def get_weather_emoji(condition):
    if condition is None:
        return "🌤️"

    condition = condition.lower()

    if "clear" in condition:
        return "☀️"

    if "cloud" in condition:
        return "☁️"

    if "rain" in condition:
        return "🌧️"

    if "snow" in condition:
        return "❄️"

    if "thunder" in condition:
        return "⛈️"

    return "🌤️"