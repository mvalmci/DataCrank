from streamlit_calendar import calendar
import streamlit as st
from datetime import datetime, timedelta
import streamlit.components.v1 as components
import streamlit as st
from streamlit_calendar import calendar
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

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

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