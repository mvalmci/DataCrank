import streamlit as st
import json
import os
from PIL import Image
from add_new_rider import load_rider_data, add_rider_to_db, PICTURE_DIR

#Streamlit settings---------------------------------------------------------------------
st.set_page_config(layout="wide")
base="dark"
primaryColor="#BF2A7C" #PINK
backgroundColor="#FFFFFF" #MAIN WINDOW BACKGROUND COLOR (white)
secondaryBackgroundColor="#EBF3FC" #SIDEBAR COLOR (light blue)
textColor="#31333F"

# Sidebar-------------------------------------------------------------------------------
st.sidebar.image(
Image.open('pictures\logo-uae.png'),
width=50, clamp=True, channels='RGB',
)
st.sidebar.markdown("# CONTACT")
st.sidebar.markdown("## UAE TEAM EMIRATES")
st.sidebar.markdown("### team@uaeteamemirates.com")
st.sidebar.markdown("## PRESS OFFICER")
st.sidebar.markdown("### Luke Maguire")
st.sidebar.markdown("### maguire@uaeteamemirates.com")
st.sidebar.markdown("## © 2025 - UAE Team Emirates")

#Haupt Code für die Seite---------------------------------------------------------------

st.title("Fahrer zur Datenbank hinzufügen")

with st.form("rider_form"):
    col1, col2 = st.columns(2)
    with col1:
        firstname = st.text_input("Vorname")
        lastname = st.text_input("Nachname")
        dob = st.number_input("Geburtsjahr", min_value=1900, max_value=2025, step=1)

    with col2:
        trainings_folder = st.text_input("Trainingsordner (z. B. Tadej_trainings)")
        image_file = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Fahrer hinzufügen")

    if submitted:
        if firstname and lastname and image_file and trainings_folder:
            # Trainingsordner prüfen
            if not os.path.isdir(trainings_folder):
                st.error(f"Trainingsordner '{trainings_folder}' wurde nicht gefunden.")
            else:
                # Bild speichern
                image_ext = image_file.name.split('.')[-1]
                image_filename = f"{lastname}_{firstname}.{image_ext}"
                picture_path = os.path.join(PICTURE_DIR, image_filename)

                os.makedirs(PICTURE_DIR, exist_ok=True)
                with open(picture_path, "wb") as f:
                    f.write(image_file.read())

                new_rider = {
                    "firstname": firstname,
                    "lastname": lastname,
                    "date_of_birth": dob,
                    "picture_path": picture_path,
                    "trainings": trainings_folder
                }

                success = add_rider_to_db(new_rider)
                if success:
                    st.success(f"{firstname} {lastname} wurde hinzugefügt.")
                    st.image(Image.open(picture_path), caption="Profilbild", width=150)
        else:
            st.error("Bitte alle Felder korrekt ausfüllen.")

# === Tabellenansicht der Rider-Datenbank ===
st.subheader("📋 Aktuelle Fahrer in der Datenbank")

rider_data = load_rider_data()
if rider_data:
    st.dataframe([
        {
            "ID": r["id"],
            "Name": f"{r['firstname']} {r['lastname']}",
            "Geburtsjahr": r["date_of_birth"],
            "Trainings": r["trainings"],
            "Bildpfad": r["picture_path"]
        }
        for r in rider_data
    ])
else:
    st.info("Noch keine Fahrer in der Datenbank.")