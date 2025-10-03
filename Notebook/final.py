# ==============================
# Streamlit Patient Activity Tracking
# ==============================

import streamlit as st
import cv2
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model
from PIL import Image

# ------------------------------
# 1️⃣ Streamlit Page Setup
# ------------------------------
st.title("🩺 Patient Activity Tracking")
st.text("Press 'Stop' to exit the stream")

# ------------------------------
# 2️⃣ Load Trained LRCN Model
# ------------------------------
model = load_model("/Users/admin/Documents/MAJOR_PROJECT2/Notebook/LRCN.h5")
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
# 4️⃣ Initialize Video Capture
# ------------------------------
video_source = st.file_uploader("Upload a video (.avi) or leave empty for webcam", type=["avi", "mp4"])
start_button = st.button("Start")
stop_button = st.button("Stop")
st.write(video_source)
if start_button:
    cap = None
    if video_source is not None:
        cap = cv2.VideoCapture(video_source.name)
    else:
        cap = cv2.VideoCapture(0)  # webcam
    
    frame_sequence = deque(maxlen=SEQUENCE_LENGTH)
    frame_window = st.image([])

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Video ended or failed to read frame.")
            break

        # Preprocess
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

        # Convert BGR → RGB for Streamlit display
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        frame_window.image(display_frame)

        # Stop button check
        if stop_button:
            break

    cap.release()
