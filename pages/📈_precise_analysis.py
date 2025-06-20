import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from read_rider_data import find_rider_data_by_name
from power_curve import aggregate_best_efforts_from_json
import os
import plotly.graph_objects as go
import calculate_statistics
import power_curve

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

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

col1, col2= st.columns([1, 1])

with col1:
    st.subheader("Precise training analysis of")

with col2:
    rider_options = ["Pogacar, Tadej", "Yates, Adam", "Del Toro, Isaac"]
    rider_selected = st.selectbox("Select rider", rider_options, key="rider_select_2")

    rider_data = find_rider_data_by_name(rider_selected)
    if rider_data:
        st.image(rider_data["picture_path"], width=100)
        st.markdown(f"**{rider_data['firstname']} {rider_data['lastname']}**")
        st.markdown(f"Date of birth: {rider_data['date_of_birth']}")
    else:
        st.error("Rider data not found.")


st.subheader("Riders statistics")
a, b, c = st.columns([1, 1, 1])

with st.spinner("Loading statistics..."):
    rider_folder = {
        "Pogacar, Tadej": ("Pogacar_Tadej"),
        "Yates, Adam": ("Yates_Adams"),
        "Del Toro, Isaac": ("Del Torro_Isaac")
    }
    if rider_selected in rider_folder:
        folder_path = rider_folder[rider_selected]
        try:
            folder = folder_path
            result = calculate_statistics.total_elevation_gain(folder)
            a.metric(f"Gesamter Elevation Gain von {rider_selected}", f"{result:.2f} hm")
        except Exception as e:
            st.error(f"Fehler beim berechnen des elevation gain: {e}")
        try:
            max_hr = calculate_statistics.max_hr(folder_path)
            b.metric(f"Höchste Herzfrequenz von {rider_selected}", f"{max_hr:.2f} bpm")
        except Exception as e:
            st.error(f"Fehler beim Berechnen der höchsten Herzfrequenz: {e}")
        try:
            total_km_value = calculate_statistics.total_km(folder)
            c.metric(f"Gesamte Kilometer in {rider_selected}", f"{total_km_value:.2f} km")
        except Exception as e:
            st.error(f"Fehler beim Berechnen der Gesamtkilometer: {e}")
    else:
        st.info("Bitte einen Fahrer auswählen, um den elevation gain zu sehen.")



with st.spinner("Loading Power Curve..."):
#Filter Buttons-------------------------------------------------------------------
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# st.subheader("Please select a Filter")
# col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# with col1:
#     btn_last = st.button("power curve last training", type="secondary")
# with col2:
#     btn_fresh = st.button("power curve fresh", type="secondary")
# with col3:
#     btn_tired = st.button("power curve tired", type="secondary")
# with col4:
#     btn_very_tired = st.button("power curve very tired", type="secondary")


#Interaktive Power Curve---------------------------------------------------------------
    rider_json_and_folder = {
        "Pogacar, Tadej": ("cycling_data_tadej.json", "Pogacar_Tadej"),
        "Yates, Adam": ("cycling_data_yates.json", "Yates_Adam"),
        "Del Toro, Isaac": ("cycling_data_toro.json", "Del_Toro_Isaac")
    }

    if rider_selected in rider_json_and_folder:
        json_path, folder_path = rider_json_and_folder[rider_selected]
        try:
            df_best = aggregate_best_efforts_from_json(json_path, folder_path)
            st.subheader("Power Curve for all trainings")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_best["Time/s"], 
                y=df_best["Best Effort"], 
                mode='lines+markers',
                name="Best Effort"
            ))
            fig.update_layout(
                xaxis_title="Time [s]",
                yaxis_title="Best Effort [W]",
                xaxis=dict(
            tickmode='array',
            tickvals=[30, 60, 180, 300, 600, 1800, 2000], 
            ticktext=["30s", "1min", "3min", "5min", "10min", "30min", "33min"]
        ),
        title=f"Power Curve: {rider_selected}",
        template="plotly_white"
    )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Fehler beim Laden oder Plotten der Power Curve: {e}")
    else:
        st.info("Bitte einen Fahrer auswählen, um die Power Curve zu sehen.")
    