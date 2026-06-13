def get_recommendation(temp, condition):

    condition = condition.lower()

    if temp > 35:
        return "🥤 Stay hydrated and avoid direct sunlight."

    if "rain" in condition:
        return "☂ Carry an umbrella."

    if temp < 15:
        return "🧥 Wear warm clothing."

    return "🌤 Pleasant weather."