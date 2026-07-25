import json
import os

CONFIG_FILE = "config.json"


def save_config(api_id, api_hash, phone):
    data = {
        "api_id": api_id,
        "api_hash": api_hash,
        "phone": phone
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return "", "", ""

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return (
        data.get("api_id", ""),
        data.get("api_hash", ""),
        data.get("phone", "")
    )