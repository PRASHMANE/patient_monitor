# ==============================
# Streamlit Patient Activity Tracking (Webcam + Uploaded Video)
# ==============================

import streamlit as st
import cv2
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model
import tempfile

# ------------------------------
# 1️⃣ Streamlit Page Setup
# ------------------------------
st.set_page_config(page_title="Patient Activity Tracking", layout="wide")
st.title("🩺 Patient Activity Tracking")
st.write("Upload a video file (.avi/.mp4) or use your webcam for live tracking.")

# ------------------------------
# 2️⃣ Load Trained LRCN Model
# ------------------------------
model_path = "/Users/admin/Documents/MAJOR_PROJECT2/Notebook/LRCN.h5"
model = load_model(model_path)
CLASSES_LIST = ['FallDown', 'Lying Down','Sit down','Sitting','stand up','standing','Walking']
SEQUENCE_LENGTH = 30
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64

# ------------------------------
# 3️⃣ Frame Preprocessing
# ------------------------------
def preprocess_frame(frame):
    frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
    frame = frame / 255.0
    return frame

# ------------------------------
# 4️⃣ Video Source Selection
# ------------------------------
uploaded_file = st.file_uploader("Upload video (.avi or .mp4)", type=["avi","mp4"])
use_webcam = st.checkbox("Use Webcam Instead", value=True)

start_button = st.button("Start Tracking")
stop_button = st.button("Stop Tracking")
temp="/Users/admin/Documents/MAJOR_PROJECT2/Notebook/"

if start_button:
    cap = None

    # ------------------------------
    # 4a️⃣ Use uploaded file
    # ------------------------------
    if uploaded_file is not None and not use_webcam:
        # Save uploaded file to temp path
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        video_path = temp_file.name
        st.write(f"Uploaded video path: f{temp/video_path}")
        cap = cv2.VideoCapture(temp/video_path)

    # ------------------------------
    # 4b️⃣ Use webcam
    # ------------------------------
    else:
        cap = cv2.VideoCapture(0)

    frame_sequence = deque(maxlen=SEQUENCE_LENGTH)
    frame_window = st.image([])

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Video ended or failed to read frame.")
            break

        # Preprocess frame
        processed = preprocess_frame(frame)
        frame_sequence.append(processed)

        # Predict activity once enough frames
        activity_text = ""
        if len(frame_sequence) == SEQUENCE_LENGTH:
            input_seq = np.expand_dims(np.array(frame_sequence), axis=0)
            preds = model.predict(input_seq, verbose=0)
            activity_index = np.argmax(preds)
            activity_text = CLASSES_LIST[activity_index]

        # Overlay activity text
        display_frame = frame.copy()
        cv2.putText(display_frame,
                    f"Activity: {activity_text}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

        # Convert BGR → RGB for Streamlit
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        frame_window.image(display_frame)

        # Stop check
        if stop_button:
            break

    # Release resources
    cap.release()
    st.success("Tracking stopped.")
