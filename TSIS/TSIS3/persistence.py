import json
import os



SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_json(filename, default_data):
    if not os.path.exists(filename):
        save_json(filename, default_data)
        return default_data

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    default_settings = {
        "sound": True,
        "car_color": "red",
        "difficulty": "normal"
    }

    return load_json(SETTINGS_FILE, default_settings)


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    return load_json(LEADERBOARD_FILE, [])


def save_score(name, score, distance):
    leaderboard = load_leaderboard()

    leaderboard.append({
        "name": name,
        "score": score,
        "distance": distance
    })

    leaderboard.sort(key=lambda item: item["score"], reverse=True)

    leaderboard = leaderboard[:10]

    save_json(LEADERBOARD_FILE, leaderboard)