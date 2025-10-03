import streamlit as st
import cv2
import time

# Page config
st.set_page_config(page_title="Webcam Stream", layout="centered")
st.title("📸 Local Webcam Live Feed")

# Toggle button
if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

if st.button("🔴 Toggle Camera"):
    st.session_state.camera_on = not st.session_state.camera_on

# Placeholder for video frame
FRAME_WINDOW = st.empty()

# Open the webcam
camera = cv2.VideoCapture(0)  # 0 = default webcam

# Display frames
while st.session_state.camera_on:
    ret, frame = camera.read()
    if not ret:
        st.error("Failed to capture video")
        break

    # Resize frame (optional, medium size)
    frame = cv2.resize(frame, (800, 600))

    # Convert BGR -> RGB for Streamlit
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display frame
    FRAME_WINDOW.image(frame)

    # Small delay to prevent high CPU usage
    time.sleep(0.03)

# Release camera when done
camera.release()
