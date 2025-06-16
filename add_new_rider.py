import streamlit as st
import json
import os
from PIL import Image

FILENAME = "rider_db.json"
PICTURE_DIR = "pictures"

def load_rider_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_rider_data(data):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_rider_to_db(new_rider):
    rider_data = load_rider_data()

    # Prüfen auf Duplikat
    for rider in rider_data:
        if rider["firstname"] == new_rider["firstname"] and rider["lastname"] == new_rider["lastname"]:
            st.warning("Fahrer existiert bereits.")
            return False

    # ID generieren
    new_id = max([r["id"] for r in rider_data], default=0) + 1
    new_rider["id"] = new_id

    rider_data.append(new_rider)
    save_rider_data(rider_data)
    return True