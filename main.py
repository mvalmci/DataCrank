import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import base64
from io import BytesIO
import plot_power_curves
from streamlit_calendar import calendar

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


# Sidebar-------------------------------------------------------------------------------
st.sidebar.image(
Image.open('pictures\logo-uae.png'),
width=50, clamp=True, channels='RGB',
)

st.sidebar.title("Upload new training")
st.sidebar.selectbox("Select rider", ["Pogacar", "Yates", "Del Toro"], key="select_rider")

customer_file = st.sidebar.file_uploader("Add to Training Database", type='csv', help='Dataset containing email address')

customer_file_valid_flag = False
if customer_file is not None:
    # Check MIME type of the uploaded file
    if  customer_file.name == "customer_data.csv":
        customer_df = pd.read_csv(customer_file)
        customer_file_valid_flag = True
        st.sidebar.success('Success')
    else:
        st.sidebar.error('Error: please, re-upload file called customer_data.csv')

#Select filters

st.sidebar.title("Current ranking")
st.sidebar.selectbox("Show best...", ["Sprinter", "Climber", "Endurance"], key="filter_select")

st.sidebar.title("Select Rider to analyze training data in detail")
st.sidebar.selectbox("Select Rider", ["Pogacar", "Yates", "Del Toro"], key="rider_select")
st.sidebar.button("Analyze", type="primary")

#neuer Abschnitt - Trainingsanalyse------------------------------------------------------
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Precise training analysis of")

with col2:
    st.selectbox("Select rider", ["Pogacar", "Yates", "Del Toro"], key="rider_select_2")


st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.button("power curve last training", type="secondary")

with col2:
    st.button("power curve after 2h", type="secondary")

with col3:
    st.button("power curve after 4h", type="secondary")

with col4:
    st.button("power curve after 5h", type="secondary")

#plot power curve for presentation, no real functions------------------------------------------


training1 = plot_power_curves.load_data("Tadej_trainings/2016_12_14_08_58_06.csv")
best_effort1 = plot_power_curves.find_best_effort(training1["power"])
figure1 = plot_power_curves.plot_power_curve(best_effort1)
st.plotly_chart(figure1, use_container_width=True)

#Race planner-------------------------------------------------------------------

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.subheader("Race planner 🏁")

# Initialize calendar
if "events" not in st.session_state:
    st.session_state["events"] = [
        {
            "title": "Tour de France",
            "color": "#FF6C6C",
            "start": "2025-07-05",
            "end": "2025-07-28",
            "resourceId": "a",
        },
        {
            "title": "Deutschland Tour",
            "color": "#FFBD45",
            "start": "2025-08-20",
            "end": "2025-08-25",
            "resourceId": "b",
        },
    ]

# UI Elements for Calendar Mode Selection
mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "timeline",
        "list",
    ),
)
# Calendar configuration options based on selected mode
calendar_options = {
    "editable": True,
    "navLinks": True,
    "selectable": True,
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "",
    },
    "initialDate": "2025-06-15",
}
if "resource" in mode:
    if mode == "daygrid":
        calendar_options.update({
            "initialView": "dayGridMonth",
            "resourceGroupField": "building",
        })
    elif mode == "timegrid":
        calendar_options.update({"initialView": "timeGridWeek"})
    elif mode == "timeline":
        calendar_options.update({
            "initialView": "timelineMonth",
        })
    elif mode == "list":
        calendar_options.update({"initialView": "listMonth"})
else:
    if mode == "daygrid":
        calendar_options.update({"initialView": "dayGridMonth"})
    elif mode == "timegrid":
        calendar_options.update({"initialView": "timeGridWeek"})
    elif mode == "timeline":
        calendar_options.update({"initialView": "timelineMonth"})
    elif mode == "list":
        calendar_options.update({"initialView": "listMonth"})  

# Create calendar instance
calendar_instance = calendar(
    events=st.session_state["events"],
    options=calendar_options,
)   