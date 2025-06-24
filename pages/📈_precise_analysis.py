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
import json

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

col1, col2= st.columns([1, 1])

with col1:
    st.subheader("Precise training analysis of")

with col2:
    rider_options = ["Pogacar, Tadej", "Yates, Adams", "Del Torro, Isaac"]
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

# Beispiel: JSON laden
with open("rider_db.json", "r", encoding="utf-8") as f:
    riders_data = json.load(f)

# Mapping wie gehabt, aber Key anpassen (siehe unten!)
rider_folder = {
    "Pogacar, Tadej": "Pogacar_Tadej",
    "Yates, Adams": "Yates_Adams",
    "Del Torro, Isaac": "Del Torro_Isaac",
    "Politt, Nils": "Politt_Nils"
}

if rider_selected in rider_folder:
    # Namen aufsplitten, um Rider in JSON zu finden
    lastname, firstname = [x.strip() for x in rider_selected.split(",", 1)]
    # Passenden Fahrer aus JSON suchen
    rider = next((r for r in riders_data if r["firstname"] == firstname and r["lastname"] == lastname), None)
    if rider:
        try:
            total_hm = rider.get("total_hm", 0)
            a.metric(f"Gesamter Elevation Gain von {rider_selected}", f"{float(total_hm):.2f} hm" if total_hm else "Keine Daten")
        except Exception as e:
            st.error(f"Fehler beim Anzeigen des elevation gain: {e}")
        try:
            max_hr = rider.get("max_hr", 0)
            b.metric(f"Höchste Herzfrequenz von {rider_selected}", f"{float(max_hr):.2f} bpm" if max_hr else "Keine Daten")
        except Exception as e:
            st.error(f"Fehler beim Anzeigen der höchsten Herzfrequenz: {e}")
        try:
            total_km = rider.get("total_km", 0)
            c.metric(f"Gesamte Kilometer in {rider_selected}", f"{float(total_km):.2f} km" if total_km else "Keine Daten")
        except Exception as e:
            st.error(f"Fehler beim Anzeigen der Gesamtkilometer: {e}")
    else:
        st.warning("Keine Statistikdaten für diesen Fahrer gefunden.")
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
    st.select_slider("Select Power Curve Phase", options=["Fresh", "Tired", "Very Tired"], value="Fresh", key="selected_phase")

    selected_phase = st.session_state.selected_phase

    rider_json_and_folder = {
        "Pogacar, Tadej": ("cycling_data_tadej.json", "Pogacar_Tadej"),
        "Yates, Adams": ("cycling_data_yates.json", "Yates_Adam"),
        "Del Torro, Isaac": ("cycling_data_toro.json", "Del_Toro_Isaac")
    }

    if rider_selected in rider_json_and_folder and selected_phase == "Fresh":
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
    
    elif rider_selected in rider_json_and_folder and selected_phase == "Tired":
        json_path, folder_path = rider_json_and_folder[rider_selected]
        try:
            tired_df, very_tired_df = power_curve.fatigue_powercurves_from_json(
                json_path, 
                windows=[30, 60, 180, 300, 600, 1800, 2000], 
                tired_limit=150000, 
                very_tired_limit=300000
            )
            st.subheader("Power Curve: Tired")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=tired_df["Time/s"], 
                y=tired_df["Best Effort"], 
                mode='lines+markers',
                name="Tired Best Effort"
            ))
            fig.update_layout(
                xaxis_title="Time [s]",
                yaxis_title="Best Effort [W]",
                xaxis=dict(
                    tickmode='array',
                    tickvals=[30, 60, 180, 300, 600, 1800, 2000], 
                    ticktext=["30s", "1min", "3min", "5min", "10min", "30min", "33min"]
                ),
                title=f"Power Curve: {rider_selected} - Tired",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Fehler beim Laden oder Plotten der Power Curve: {e}")
    elif rider_selected in rider_json_and_folder and selected_phase == "Very Tired":
        json_path, folder_path = rider_json_and_folder[rider_selected]
        try:
            tired_df, very_tired_df = power_curve.fatigue_powercurves_from_json(
                json_path, 
                windows=[30, 60, 180, 300, 600, 1800, 2000], 
                tired_limit=150000, 
                very_tired_limit=300000
            )
            st.subheader("Power Curve: Very Tired")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=very_tired_df["Time/s"], 
                y=very_tired_df["Best Effort"], 
                mode='lines+markers',
                name="Very Tired Best Effort"
            ))
            fig.update_layout(
                xaxis_title="Time [s]",
                yaxis_title="Best Effort [W]",
                xaxis=dict(
                    tickmode='array',
                    tickvals=[30, 60, 180, 300, 600, 1800, 2000], 
                    ticktext=["30s", "1min", "3min", "5min", "10min", "30min", "33min"]
                ),
                title=f"Power Curve: {rider_selected} - Very Tired",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Fehler beim Laden oder Plotten der Power Curve: {e}")
    else:
        st.info("Bitte einen Fahrer auswählen, um die Power Curve zu sehen.")