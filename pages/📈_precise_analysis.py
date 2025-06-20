import streamlit as st
import power_curve
from PIL import Image
import base64
from io import BytesIO
from read_rider_data import find_rider_data_by_name

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

col1, col2 = st.columns([1, 1])

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
    


st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

st.subheader("Please select a Filter")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.button("power curve last training", type="secondary")

with col2:
    st.button("power curve fresh", type="secondary")

with col3:
    st.button("power curve tired", type="secondary")

with col4:
    st.button("power curve very tired", type="secondary")

#plot power curve for presentation, no real functions------------------------------------------


training1 = power_curve.load_data("Pogacar_Tadej/2016_12_14_08_58_06.csv")
best_effort1 = power_curve.find_best_effort(training1["power"])
figure1 = power_curve.plot_power_curve(best_effort1)
st.plotly_chart(figure1, use_container_width=True)