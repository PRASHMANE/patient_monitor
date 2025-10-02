def remove_pat_info(id):
    import yaml
    import streamlit as st
    import shutil

    # Load the YAML file
    with open("deployment/api/pat_info/patient.yaml", "r") as file:
        data = yaml.safe_load(file) or {}
    # Check if USN exists
    if id in data:
        del data[id]  # Remove the entire USN entry

        # Write back to the file
        with open("deployment/api/pat_info/patient.yaml", "w") as file:
            yaml.safe_dump(data, file, sort_keys=False)

        #st.write(f"Removed all details for USN: {usn}")

        def find_image(id):
        # Try different extensions
            extensions = [".jpg", ".jpeg", ".png", ".gif"]
            for ext in extensions:
                path = os.path.join(IMAGE_DIR, f"{id}{ext}")
                if os.path.exists(path):
                    return path
            return None  # If no image found

        import os
        IMAGE_DIR = "deployment/api/pat_img"
        file_path = find_image(id)   # or .jpg, .jpeg, etc.

        
        #shutil.rmtree(folder_path)  # deletes non-empty folder
        if os.path.exists(file_path):
            os.remove(file_path)
            st.write("Image deleted successfully.")
        else:
            st.write("Image not found.")


        import os

        folder_path = f"data/{id}"

        if os.path.exists(folder_path):
            #os.rmdir(folder_path)  # works only if the folder is empty
            shutil.rmtree(folder_path)
            st.write("Folder deleted successfully.")
        else:
            #st.write("Folder not found.")
            pass
        st.write(f"✅ Removed all details and associated image for ID: {id}")

    else:
        st.write(f"No entry found for ID: {id}")

