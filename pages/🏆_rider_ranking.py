import streamlit as st
from PIL import Image
import base64
from io import BytesIO

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

# Main window---------------------------------------------------------------------------
st.subheader("Top 3 rider over all categories")

# Ranking

col1, col2, col3 = st.columns(3)

with col1:
    st.image("pictures\DelToro.png", use_column_width=True)
    st.markdown("**Best Climber ⛰️**<br>FTP: 350 / Hours of training today: 4,5h", unsafe_allow_html=True)
    if st.button("Plan for upcoming Hill Stage", type="primary"):
        st.write("Planned for upcoming Hill Stage ✅")

with col2:
    st.image("pictures\Pogacar.png", use_column_width=True)
    st.markdown("**Best Sprinter 📈**<br>FTP: 350 / Hours of training today: 4,5h", unsafe_allow_html=True)
    if st.button("Plan for upcoming Sprint Stage", type="primary"):
        st.write("Planned for upcoming Sprint Stage ✅")

with col3:
    st.image("pictures\Yates.png", use_column_width=True)
    st.markdown("**Best over all categories 🔥**<br>FTP: 350 / Hours of training today: 4,5h", unsafe_allow_html=True)
    if st.button("Plan for upcoming race", type="primary"):
        st.write("Planned for upcoming Race ✅")