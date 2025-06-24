import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import func_rider_ranking
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


st.subheader("Top 3 rider over all categories")

# Ranking

col1, col2, col3 = st.columns(3)

with col1:

    with open("rider_db.json", "r", encoding="utf-8") as file:
        riders = json.load(file)

    statistik = func_rider_ranking.get_sorted_riders_by_elevation(riders)
    best_climber = statistik[0]
    
    st.image(best_climber["picture_path"], use_column_width=True)
    st.markdown("**Best Climber ⛰️**<br>FTP: 350 / Hours of training today: 4,5h", unsafe_allow_html=True)
    if st.button("Plan for upcoming Hill Stage", type="primary"):
        st.write("Planned for upcoming Hill Stage ✅")

with col2:
    st.image("pictures/Pogacar.png", use_column_width=True)
    st.markdown("**Best Sprinter 📈**<br>FTP: 350 / Hours of training today: 4,5h", unsafe_allow_html=True)
    if st.button("Plan for upcoming Sprint Stage", type="primary"):
        st.write("Planned for upcoming Sprint Stage ✅")

with col3:
    st.image("pictures/Yates.png", use_column_width=True)
    st.markdown("**Best over all categories 🔥**<br>FTP: 350 / Hours of training today: 4,5h", unsafe_allow_html=True)
    if st.button("Plan for upcoming race", type="primary"):
        st.write("Planned for upcoming Race ✅")