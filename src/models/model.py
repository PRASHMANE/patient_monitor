from src.models.alert import send_email_alert
def track():
    import streamlit as st
    import cv2
    import numpy as np
    from collections import deque
    from tensorflow.keras.models import load_model
    from ultralytics import YOLO
    from deep_sort_realtime.deepsort_tracker import DeepSort
    import tempfile
    import os

    # ------------------------------
    # Load Models
    # ------------------------------
    yolo = YOLO("yolov8n.pt")   # for detecting persons
    tracker = DeepSort(max_age=30)  # for tracking IDs
    model = load_model("/Users/admin/Documents/MAJOR_PROJECT2/LRCN_model_saved.h5")  # your trained activity model

    CLASSES_LIST = ['FallDown','Lying Down','Sit down','Sitting','stand up','standing','Walking']
    SEQUENCE_LENGTH = 30
    IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
    trk={}
    # ------------------------------
    # Preprocess
    # ------------------------------
    def preprocess_frame(frame):
        frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        return frame / 255.0

    # ------------------------------
    # Streamlit UI
    # ------------------------------
    #st.set_page_config(page_title="Patient Tracking", layout="wide")
    st.title("🩺 Patient Tracking System")
    uploaded_file = st.file_uploader("Upload video (.mp4/.avi)", type=["mp4","avi"])
    use_webcam = st.checkbox("Use Webcam Instead")
    start_button = st.button("▶️ Start Tracking")
    stop_button = st.button("⏹️ Stop Tracking")

    if start_button:
        if uploaded_file is not None and  use_webcam:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())
            cap = cv2.VideoCapture(temp_file.name)
        else:
            cap = cv2.VideoCapture(0)  # webcam

        frame_window = st.image([])
        patient_buffer = {}  # per-person frame buffer

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("Video ended or cannot read frames.")
                break

            # Step 1: detect people
            results = yolo(frame, classes=[0])  # class 0 = person
            detections = []
            for box in results[0].boxes.xyxy:
                x1,y1,x2,y2 = map(int, box)
                detections.append(([x1,y1,x2-x1,y2-y1], 0.99, 'person'))

            # Step 2: track people
            tracks = tracker.update_tracks(detections, frame=frame)

            for track in tracks:
                if not track.is_confirmed():
                    continue
                track_id = track.track_id
                l,t,r,b = track.to_ltrb()
                crop = frame[int(t):int(b), int(l):int(r)]

                if crop.size == 0:
                    continue

                processed = preprocess_frame(crop)

                # save buffer per ID
                if track_id not in patient_buffer:
                    patient_buffer[track_id] = deque(maxlen=SEQUENCE_LENGTH)
                patient_buffer[track_id].append(processed)

                activity = ""
                if len(patient_buffer[track_id]) == SEQUENCE_LENGTH:
                    seq = np.expand_dims(np.array(patient_buffer[track_id]), axis=0)
                    preds = model.predict(seq, verbose=0)
                    activity = CLASSES_LIST[np.argmax(preds)]

                # draw box + activity
                cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0,255,0), 3)
                cv2.putText(frame, f"ID {track_id}: {activity}",
                            (int(l), int(t)-10), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0,0,255), 3, cv2.LINE_AA)
                if track_id not in trk:
                    trk[track_id]=activity
                else:
                    if  activity == "Walking" and trk[track_id] != "Walking":
                        trk[track_id]=activity
                        pass
                    elif activity != "Walking":
                        trk[track_id]=activity
            # BGR → RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_window.image(frame_rgb)

            if stop_button:
                break

        cap.release()
        st.success("Tracking stopped ✅")

        # cleanup uploaded file
        if uploaded_file is not None and not use_webcam:
            os.remove(temp_file.name)
