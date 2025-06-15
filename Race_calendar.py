from streamlit_calendar import calendar
import streamlit as st
from datetime import datetime, timedelta
import os
import streamlit.components.v1 as components

import streamlit as st
from streamlit_calendar import calendar

# Set page configuration
st.set_page_config(page_title="Demo for Streamlit Calendar", page_icon="📆")

# Initialize events data
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
        calendar_options.update({
            "initialView": "timelineMonth",
        })
    elif mode == "list":
        calendar_options.update({"initialView": "listMonth"})

# Calendar component
calendar_instance = calendar(
    events=st.session_state["events"],
    options=calendar_options,
    custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
    """,
    key=mode,
)
updated_calendar_instance = None

# Update session state with events from calendar instance
if "eventsSet" in calendar_instance:
    st.session_state["events"] = calendar_instance["eventsSet"]
st.write(calendar_instance)