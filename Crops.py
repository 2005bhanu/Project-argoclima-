# pages/_Image_Gallery.py
import streamlit as st
import os
import random

st.set_page_config(
    page_title="Crops",
    page_icon="📸",
    layout="wide"
)

st.title("Crops Image Gallery")

st.write("")

# --- Determine the correct path to the images directory ---
# This assumes _Image_Gallery.py is in 'project/pages'
# and images are in 'project/images'
# So, from 'pages', we go up one level (..) to 'project', then into 'images'

# Get the directory of the current script (_Image_Gallery.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the images directory
IMAGE_DIR = os.path.join(SCRIPT_DIR, '..', 'cropic')

# Check if the directory exists
if not os.path.exists(IMAGE_DIR):
    st.error(f"The 'images' directory does not exist at: {IMAGE_DIR}. Please create it and add images.")
else:
    # List all files in the images directory
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]

    if not image_files:
        st.warning(f"No image files found in the '{IMAGE_DIR}' directory. Please add some images.")
    else:
        st.write(f"Found {len(image_files)} images.")

        # Optional: Add a search/filter by restaurant if you link images to data
        # (This would require a way to map image filenames to restaurant names)

        # Display images in columns
        num_columns = 3 # You can adjust this number
        columns = st.columns(num_columns)

        # Shuffle images for varied display
        random.shuffle(image_files)

        for i, image_file in enumerate(image_files):
            with columns[i % num_columns]: # Cycle through columns
                image_path = os.path.join(IMAGE_DIR, image_file)
                try:
                    # CHANGED THIS LINE:
                    st.image(image_path, caption=image_file, use_container_width=True)
                except Exception as e:
                    st.warning(f"Could not load image {image_file}: {e}")