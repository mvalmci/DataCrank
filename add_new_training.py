import streamlit as st
import pandas as pd
import os
import json
import calculate_statistics

st.title("Upload new training")

rider_options = ["Pogacar, Tadej", "Yates, Adams", "Del Torro, Isaac"]
rider = st.selectbox("Select rider", rider_options, key="rider_select")

uploaded_file = st.file_uploader("Add to Training Database", type='csv', help='Dataset containing training data')

def new_training(rider, uploaded_file):
    if uploaded_file is not None:
        try:
            #st.write("Start read")
            df = pd.read_csv(uploaded_file)
            #st.write("Read done")

            folder_name = rider.replace(", ", "_")
            folder_path = folder_name
            os.makedirs(folder_path, exist_ok=True)
            #st.write("Folder created")

            csv_path = os.path.join(folder_path, uploaded_file.name)
            with open(csv_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            #st.write("CSV saved")

            json_path = os.path.join(folder_path, "training_data.json")
            # Dummy function for testing
            success, message = True, "Training erfolgreich verarbeitet"
            #st.write("process_training_file done")

            if success:
                st.success(message)
            else:
                st.warning(message)

        except Exception as e:
            st.error(f"Fehler beim Verarbeiten der Datei: {e}")



def safe_statistics_to_json(lastname, firstname):
    FILENAME = "rider_db.json"

    # Bestehende Daten laden
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as file:
            riders = json.load(file)
    else:
        riders = []

    # Rider in der Liste suchen
    for rider in riders:
        if rider["firstname"] == firstname and rider["lastname"] == lastname:
            folder_path = rider["trainings"]  # oder wie du den Ordner bestimmst

            # Statistiken berechnen und eintragen
            rider["total_km"] = calculate_statistics.total_km(folder_path, distance_column='km')
            rider["total_hm"] = calculate_statistics.total_elevation_gain(folder_path, altitude_column='alt')
            rider["max_hr"] = calculate_statistics.max_hr(folder_path, hr_column='hr')
            break
    else:
        # Rider nicht gefunden, optional: Fehler oder neuen Rider anlegen
        st.error(f"Rider mit lastname {lastname} nicht gefunden!")
        return False

    # Speichern
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(riders, file, ensure_ascii=False, indent=2)

    st.success(f"Statistics for rider {lastname} saved to {FILENAME}")
    return True
