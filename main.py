import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import base64
from io import BytesIO
from streamlit_calendar import calendar
from sort_data import process_training_file
import os

#Streamlit settings---------------------------------------------------------------------
st.set_page_config(layout="wide")
base="dark"
primaryColor="#BF2A7C" #PINK
backgroundColor="#FFFFFF" #MAIN WINDOW BACKGROUND COLOR (white)
secondaryBackgroundColor="#EBF3FC" #SIDEBAR COLOR (light blue)
textColor="#31333F"

#Code für Bild mit Overlay-Text---------------------------------------------------------
image_path = r"pictures/Team-header-826840676.jpg"

# Bild laden und in base64 umwandeln----------------------------------------------------
def get_base64_image(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

img_base64 = get_base64_image(image_path)

# HTML anzeigen-------------------------------------------------------------------------
st.markdown(f"""
<div style="position: relative; width: 100%; overflow: hidden;">
    <img src="data:image/jpeg;base64,{img_base64}" 
         style="width: 100%; height: 100%; object-fit: cover; filter: brightness(25%);">
    <h1 style="position: absolute; top: 50%; left: 50%;
               transform: translate(-50%, -50%);
               color: white; font-size: 3em; margin: 0;">
        UAE training analyzer
    </h1>
</div>
""", unsafe_allow_html=True)


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



#Home Page------------------------------------------------------------------------------

st.title("Upload new training")

rider_options = ["Pogacar, Tadej", "Yates, Adam", "Del Toro, Isaac"]
rider = st.selectbox("Select rider", rider_options, key="rider_select")

uploaded_file = st.file_uploader("Add to Training Database", type='csv', help='Dataset containing training data')

if uploaded_file is not None:
    try:
        #st.write("Start read")
        df = pd.read_csv(uploaded_file)
        #st.write("Read done")

        folder_name = rider.replace(", ", "_").replace(" ", "_")
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

