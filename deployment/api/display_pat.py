def pat_display():
    import streamlit as st
    import yaml
    from PIL import Image
    import os

    # Path to YAML file
    YAML_FILE = "deployment/api/pat_info/patient.yaml"
    IMAGE_DIR = "deployment/api/pat_img"

    def load_students():
        with open(YAML_FILE, "r") as file:
            return yaml.safe_load(file) or {}

    def find_image(id):
        # Try different extensions
        extensions = [".jpg", ".jpeg", ".png", ".gif"]
        for ext in extensions:
            path = os.path.join(IMAGE_DIR, f"{id}{ext}")
            if os.path.exists(path):
                return path
        return None  # If no image found

    # UI
    #st.set_page_config(layout="wide")

    st.title("🧑‍⚕️ Patient Information")

    # Input USN
    id = st.text_input("Enter patient ID:")

    if id:
        students = load_students()
        
        if id in students:
            image_path = find_image(id)
            
            col1, col2 = st.columns([1,2])
            
            with col1:
                if image_path:
                    img = Image.open(image_path)
                    st.image(img, caption=f"USN: {id}", use_container_width=True)
                else:
                    st.warning("⚠️ No image found for this paatient")
            
            with col2:
                st.subheader("📋 Student Details")
                for i, details in enumerate(students[id], start=1):
                    st.markdown(f"**Record {i}:**")
                    st.write(details)
        else:
            st.error("❌ Patient ID not found in records")
