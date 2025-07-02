import streamlit as st
from PIL import Image
import io
import func_rider_ranking
import json

#Streamlit settings---------------------------------------------------------------------
st.set_page_config(layout="wide")
base="dark"
textColor="#31333F"

# Sidebar-------------------------------------------------------------------------------
st.sidebar.image(
Image.open('pictures/logo-uae.png'),
width=50, clamp=True, channels='RGB',
)
st.sidebar.markdown("# CONTACT")
st.sidebar.markdown("## UAE TEAM EMIRATES")
st.sidebar.markdown("### team@uaeteamemirates.com")
st.sidebar.markdown("## PRESS OFFICER")
st.sidebar.markdown("### Luke Maguire")
st.sidebar.markdown("### maguire@uaeteamemirates.com")
st.sidebar.markdown("## © 2025 - UAE Team Emirates")


st.subheader("Top rider in each category")

#ranking
col1, col2 = st.columns(2)

with col1:

    with open("rider_db.json", "r", encoding="utf-8") as file:
        riders = json.load(file)

    statistik = func_rider_ranking.get_sorted_riders_by_elevation(riders)
    best_climber = statistik[0]
    
    st.image(best_climber["picture_path"], use_column_width=True)
    st.write(best_climber["firstname"], best_climber["lastname"])
    st.markdown("**Best Climber ⛰️**", unsafe_allow_html=True)
    if st.button("Plan for upcoming Hill Stage", type="primary"):
        st.write("Planned for upcoming Hill Stage ✅")

with col2:

    with open("rider_db.json", "r", encoding="utf-8") as file:
        riders = json.load(file)

    sprinter = func_rider_ranking.get_best_sprinter(riders)
    best_sprinter = sprinter[0]

    st.image(best_sprinter["picture_path"], use_column_width=True)
    st.write(best_sprinter["firstname"], best_sprinter["lastname"])
    st.markdown("**Best Sprinter 📈**", unsafe_allow_html=True)
    if st.button("Plan for upcoming Sprint Stage", type="primary"):
        st.write("Planned for upcoming Sprint Stage ✅")