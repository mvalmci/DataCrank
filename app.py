import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import base64
from io import BytesIO
from streamlit_calendar import calendar
from sort_data import process_training_file
import os
import add_new_training

#Streamlit settings---------------------------------------------------------------------
st.set_page_config(layout="wide")
base="dark"

#Code für Bild mit Overlay-Text---------------------------------------------------------
image_path = r"pictures/Team-header-826840676.jpg"

#in base64 umwandeln----------------------------------------------------
def get_base64_image(path):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

img_base64 = get_base64_image(image_path)

#HTML-------------------------------------------------------------------------
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


#Sidebar-------------------------------------------------------------------------------
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

rider_options = ["Pogacar, Tadej", "Yates, Adams", "Del Torro, Isaac"]
rider = st.selectbox("Select rider", rider_options, key="rider_select")

uploaded_file = st.file_uploader("Add to Training Database", type='csv', help='Dataset containing training data')

add_new_training.new_training(rider, uploaded_file)

lastname, firstname = [part.strip() for part in rider.split(",", maxsplit=1)]
add_new_training.safe_statistics_to_json(lastname, firstname)


