def home():
    import streamlit as st

    # ------------------------------
    # 1️⃣ Page Title & Introduction
    # ------------------------------
    #st.set_page_config(page_title="Patient Activity Tracking", layout="wide")
    st.title("🩺 Patient Activity Tracking System")

    st.markdown("""
    Welcome to the **Patient Activity Tracking Project**.  
    This system uses AI and computer vision to monitor patient activities such as walking, sitting, lying down, or falling.  
    It is designed to assist healthcare professionals in tracking patient movements in real-time using webcams or uploaded videos.
    """)

    # ------------------------------
    # 2️⃣ Two Columns: Students + Image
    # ------------------------------
    col1, col2 = st.columns([1, 2])

    # Left Column → Student Names
    with col1:
        st.subheader("Team Members")
        students = ["GANASREE A (1AJ22CS049)", "Student 2", "Student 3"]
        for s in students:
            st.write(f"- {s}")

    # Right Column → Image/Logo
    with col2:
        st.subheader("Project Logo")
        st.image("patient_logo.jpeg", use_container_width=True)  # replace with your image path
