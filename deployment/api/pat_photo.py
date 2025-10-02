
def pat_photo(id,uploaded_file):
    import streamlit as st
    import os

    st.title("📸 Image Uploader")

    patient_id=id

    # Define directory to save images
    SAVE_DIR = "deployment/api/pat_img"

    os.makedirs(SAVE_DIR, exist_ok=True)


    # Upload image
    #uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    #save_photo = st.form_submit_button("Save Photo")


    if uploaded_file is not None:
        # Show preview
        #st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        import imghdr

        file_type = imghdr.what(uploaded_file)

        new_filename = f"{patient_id}.{file_type}" 

        # Save file in the uploads directory
        save_path = os.path.join(SAVE_DIR, new_filename)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ Image saved successfully as {patient_id} in '{SAVE_DIR}' folder")

