import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import sys
import os

# --- PASTE YOUR BASE64 STRING HERE ---
# Replace 'YOUR_BASE64_IMAGE_STRING_HERE' with the actual string you copied.
# Make sure to include 'data:image/jpeg;base64,' or 'data:image/png;base64,' prefix.
# Adjust 'jpeg'/'png' based on your image type.
BASE64_IMAGE_STRING = "data:image/jpeg;base64,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"

st.markdown(
    f"""
    <style>
    /* This targets the main Streamlit app container */
    .stApp {{
        background-image: url("{BASE64_IMAGE_STRING}"); /* Set background image */
        background-size: cover; /* Cover the entire area */
        background-position: center; /* Center the image */
        background-repeat: no-repeat; /* Do not repeat the image */
        background-attachment: fixed; /* Keep image fixed when scrolling */
        background-color: #75bfff; /* Fallback color if image fails to load */
        color: #FFFFFF; /* Darker text color for better contrast on light background */
    }}

    /* This targets the main content block */
    .block-container {{
        # background-color: rgba(173, 216, 230, 0.7); /* Light blue background with transparency */
        # padding: 2rem;
        # border-radius: 0.5rem;
        # box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }}

    /* --- SIDEBAR STYLING --- */
    .stSidebar {{
        background-color: rgba(252, 238, 223, 0.8); /* Lighter orange/peach with transparency */
        color: #000000; /* Black for general sidebar text (this might be overridden by Streamlit's internal link styling) */
    }}

    /* Adjust the text color for the sidebar navigation links */
    .stSidebar a {{
        color: #000000 !important; /* Black for sidebar links for contrast on light background */
        font-weight: bold;
    }}
    /* When a sidebar link is active/selected */
    .stSidebar a.active {{
        color: #0000FF !important; /* Blue for active link */
    }}
    /* Hover state for sidebar links */
    .stSidebar a:hover {{
        color: #87CEEB !important; /* Lighter blue on hover */
    }}

    /* --- END OF SIDEBAR STYLING --- */

    /* Adjust the text color for general headers */
    h1, h2, h3, h4, h5, h6 {{
        color: #0000FF; /* Blue for headings */
    }}

    /* Adjust the success message styling */
    .stSuccess {{
        background-color: #D4EDDA !important; /* Lighter green for success message background */
        color: #000000 !important; /* Black for the success message text */
        border-color: #C3E6CB !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# NEW: Correctly add the directory where app.py resides to the Python path.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the load_and_clean_data function and data paths from the utils folder
from utils.data_loader import load_and_clean_data, VEG_DATA_PATH, WEATHER_DATA_PATH

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Hoshiarpur Crop & Weather Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Main Page Content (Home Page) ---
st.title("Welcome to the Hoshiarpur Crop & Weather Analysis App!")
st.markdown("""
This application provides insightful analysis into the trends of vegetable prices (Capsicum, Carrot, Potato)
in Hoshiarpur, Punjab, and explores their relationship with local weather conditions over the past 5 years.

**Key features of this application include:**
- **Overview Dashboard**: Get a high-level summary of both datasets and overall market and weather trends.
- **Crop-Specific Analysis**: Dive deep into individual crop price movements, seasonal patterns, and their direct correlation with various weather parameters.
- **Comparative Analysis**: Compare price trends across multiple vegetables or analyze weather patterns across different years to identify broader influences.
- **Dedicated Crop-Weather Comparison Pages**: Specific pages for detailed analysis of each crop (Carrot, Capsicum, Potato) against relevant weather factors.
- **Seasonal Trends**: A dedicated section to visualize and understand how prices and weather vary across different months and seasons over the years.
- **About Page**: Provides information about the project's objectives, data sources, and development details.

To get started, please select a page from the sidebar on the left.
""")

# You can optionally add some quick stats or a small chart here for the home page
# For example, a quick summary of the data loaded:
st.subheader("Quick Data Load Status:")
df_veg, df_wea, df_combined = load_and_clean_data(VEG_DATA_PATH, WEATHER_DATA_PATH)

if df_combined is not None:
    st.success("All data loaded and preprocessed successfully!")
    st.write(f"**Total Records:** {len(df_combined)} in the combined dataset.")
    st.write(f"**Date Range:** {df_combined['Date'].min().strftime('%Y-%m-%d')} to {df_combined['Date'].max().strftime('%Y-%m-%d')}")
    st.write(f"**Crops Covered:** {', '.join(df_combined['Vegetable'].unique())}")
else:
    st.error("Failed to load data. Please check the console for detailed error messages and ensure your data files are correctly placed in the `data/` directory.")