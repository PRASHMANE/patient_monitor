import streamlit as st
import requests
import numpy as np
import cv2
from streamlit_autorefresh import st_autorefresh

st.header("📷 Add Camera URL")
st.title("📷 IP Camera Live Feed")

        # Input URL
if "url_input" not in st.session_state:
    st.session_state.url_input = ""

    st.session_state.url_input = st.text_input("Enter Camera Stream URL (e.g., http://IP:8080)", st.session_state.url_input)
    camera_on = st.checkbox("Camera ON/OFF")

        # Placeholder
    FRAME_WINDOW = st.empty()
    ERROR_WINDOW = st.empty()

        # Auto-refresh every 100ms
    st_autorefresh(interval=100, key="video_refresh")

    if camera_on and st.session_state.url_input.strip() != "":
        url = st.session_state.url_input.strip()
        if not url.endswith("shot.jpg"):
            url = f"{url}/shot.jpg"

            try:
                img_resp = requests.get(url, timeout=5)
                img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    FRAME_WINDOW.image(frame)
                    ERROR_WINDOW.empty()
                else:
                    ERROR_WINDOW.warning("Failed to capture frame from camera.")

            except requests.exceptions.RequestException:
                ERROR_WINDOW.warning("⚠️ Cannot reach the camera URL. Please check the URL or network.")

            except Exception as e:
                ERROR_WINDOW.warning(f"⚠️ Unexpected error: {e}")

        elif camera_on:
            ERROR_WINDOW.warning("Please enter a valid URL!")