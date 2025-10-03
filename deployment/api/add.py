def add_patient():
    import streamlit as st
    import os
    import time
    from deployment.api.patient_info import patient_info
    from deployment.api.pat_photo import pat_photo
    #from std_info import std_info
    #from Student_Detils import std_det
    #from Student_photo import Std_photo
    #from rec_add import add_audio

    #import streamlit as st
    #import os
    #import time
    #from std_info import std_info  # your function that saves details

    # ---------- Init persistent state ----------
    if "id" not in st.session_state:
        st.session_state.id = ""

    #st.title(" patient Information System")

    # One global USN used across all pages
    st.text_input("id (used for all sections)", key="id", help="This id will be used when saving details and photos")

    # Horizontal navigation via tabs (stable, no flicker)
    tab1, tab2 = st.tabs(["📝 patient Details", "📸 Upload Photo"])

    # ---------------- 1) Student Details ----------------
    with tab1:
        with st.form("details_form", clear_on_submit=False):
            name = st.text_input("Name")
            age = st.text_input("age")
            phone = st.text_input("Phone No.")
            save_details = st.form_submit_button("Save Details")

            if save_details:
                id = st.session_state.id.strip()
                if not id:
                    st.warning("Please enter the ID at the top before saving.")
                else:
                    # Ensure per-student fold
                    # Your existing save function
                    patient_info(id, name, age, phone)

                    st.success(f"✅ Details saved for ID {id}")

    # ---------------- 2) Upload Photo ----------------
    with tab2:
        with st.form("photo_form", clear_on_submit=False):
            uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
            save_photo = st.form_submit_button("Save Photo")
            if save_photo:
                id = st.session_state.id.strip()
                if not id:
                    st.warning("Please enter the id at the top before saving the photo.")
                
                else:
                    pat_photo(id,uploaded_file)
                    st.success(f"✅ Photo saved for ID {id}")
                

