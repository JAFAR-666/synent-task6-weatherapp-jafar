import json

FILE_PATH = "data/favorites.json"


def load_favorites():

    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    except:
        return {"cities": []}


def save_favorites(data):

    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def add_city(city):

    data = load_favorites()

    if city not in data["cities"]:
        data["cities"].append(city)

    save_favorites(data)