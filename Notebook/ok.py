st.header("📷 Add Camera URL")
        import streamlit as st
        import requests
        import numpy as np
        import cv2
        import time

        st.title("📷 IP Camera Live Feed")

        # Input URL
        url_input = st.text_input("Enter Camera Stream URL (e.g., http://IP:8080)")
        camera_on = st.checkbox("Camera ON/OFF")

        # Placeholder
        FRAME_WINDOW = st.empty()

        if camera_on and url_input.strip() != "":
            url = url_input.strip()
            if not url.endswith("shot.jpg"):
                url = f"{url}/shot.jpg"

            # Poll camera continuously
            while camera_on:
                try:
                    img_resp = requests.get(url, timeout=5)
                    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
                    frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        FRAME_WINDOW.image(frame)
                    else:
                        st.warning("Failed to capture frame")
                        
                    time.sleep(0.1)  # small delay for polling
                except Exception as e:
                    st.error(f"Error fetching frame: {e}")
                    break