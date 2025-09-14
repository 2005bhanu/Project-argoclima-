import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_and_clean_data, VEG_DATA_PATH, WEATHER_DATA_PATH

# Set page configuration at the very beginning
st.set_page_config(
    page_title="Hoshiarpur Crop & Weather Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    /* This targets the main Streamlit app container */
    .stApp {
        background-color: #DAE8F6; /* Light grey background */
        color: #333333; /* Darker text color for better contrast on light background */
    }

    /* This targets the main content block */
    .block-container {
        background-color: #a1eaf8; /* Light blue background for the main content area */
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    /* --- SIDEBAR STYLING --- */
    .stSidebar {
        background-color: #F6E8DA; /* Dark blue for the sidebar background */
        color: #D3CDFE; /* Black for general sidebar text (this might be overridden by Streamlit's internal link styling) */
    }

    /* Adjust the text color for the sidebar navigation links */
    .stSidebar a {
        color: #FFFFFF !important; /* White for sidebar links for contrast on dark blue */
        font-weight: bold;
    }
    /* When a sidebar link is active/selected */
    .stSidebar a.active {
        color: #DAE8F6 !important; /* Gold for active link */
    }
    /* Hover state for sidebar links */
    .stSidebar a:hover {
        color: #FFFAF0 !important; /* Lighter white/cream on hover */
    }

    /* --- END OF SIDEBAR STYLING --- */

    /* Adjust the text color for general headers */
    h1, h2, h3, h4, h5, h6 {
        color: #0000FF; /* Blue for headings */
    }

    /* Adjust the success message styling */
    .stSuccess {
        background-color: #D4EDDA !important; /* Lighter green for success message background */
        color: #000000 !important; /* Black for the success message text */
        border-color: #C3E6CB !important; /* Border color for success message */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data (this will be cached by Streamlit)
# The load_and_clean_data function is assumed to be in utils/data_loader.py
# For this example, a dummy implementation will be provided for utils/data_loader.py
df_veg, df_wea, df_combined = load_and_clean_data(VEG_DATA_PATH, WEATHER_DATA_PATH)

# Check if data loaded successfully
if df_combined is None:
    st.error("Data loading failed. Please check data files and paths in utils/data_loader.py.")
    st.stop() # Stop the app if data loading failed

st.title("📈 Hoshiarpur Crop & Weather Overview Dashboard")

st.markdown("This dashboard provides a high-level overview of the combined vegetable sales and weather data.")

# Display summary statistics
st.header("📊 Data Summaries")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Vegetable Sales Data (First 5 Rows)")
    st.dataframe(df_veg.head())
    st.subheader("Vegetable Sales Data Description")
    st.dataframe(df_veg.describe(include='all'))

with col2:
    st.subheader("Weather Data (First 5 Rows)")
    st.dataframe(df_wea.head())
    st.subheader("Weather Data Description")
    st.dataframe(df_wea.describe(include='all'))

st.header("Combined Data Overview")
st.write(f"Total records in combined dataset: **{len(df_combined)}**")
st.write(f"Date Range: **{df_combined['Date'].min().strftime('%Y-%m-%d')}** to **{df_combined['Date'].max().strftime('%Y-%m-%d')}**")
st.write(f"Crops analyzed: **{', '.join(df_combined['Vegetable'].unique())}**")

# Overall Modal Price Trend
st.header("Overall Modal Price Trend Over Time")
fig_price_trend = px.line(
    df_combined.groupby('Date')['Modal_Price'].mean().reset_index(),
    x='Date',
    y='Modal_Price',
    title='Average Modal Price Across All Vegetables Over Time',
    labels={'Modal_Price': 'Average Modal Price (Rs./Quintal)', 'Date': 'Date'}
)
st.plotly_chart(fig_price_trend, use_container_width=True)

# Average Modal Price by Vegetable
st.header("Average Modal Price by Vegetable")
avg_price_by_veg = df_combined.groupby('Vegetable')['Modal_Price'].mean().reset_index()
fig_avg_veg_price = px.bar(
    avg_price_by_veg,
    x='Vegetable',
    y='Modal_Price',
    title='Average Modal Price per Vegetable',
    labels={'Modal_Price': 'Average Modal Price (Rs./Quintal)'},
    color='Vegetable'
)
st.plotly_chart(fig_avg_veg_price, use_container_width=True)

# Average Temperature and Precipitation Trend
st.header("Average Temperature and Precipitation Trend Over Time")
col_temp, col_prcp = st.columns(2)
with col_temp:
    temp_trend = df_wea.groupby('Date')['Avg_Temp_C'].mean().reset_index()
    fig_temp_trend = px.line(
        temp_trend,
        x='Date',
        y='Avg_Temp_C',
        title='Average Daily Temperature (°C)',
        labels={'Avg_Temp_C': 'Average Temperature (°C)', 'Date': 'Date'}
    )
    st.plotly_chart(fig_temp_trend, use_container_width=True)
with col_prcp:
    prcp_trend = df_wea.groupby('Date')['Precipitation_mm'].sum().reset_index()
    fig_prcp_trend = px.line(
        prcp_trend,
        x='Date',
        y='Precipitation_mm',
        title='Total Daily Precipitation (mm)',
        labels={'Precipitation_mm': 'Precipitation (mm)', 'Date': 'Date'}
    )
    st.plotly_chart(fig_prcp_trend, use_container_width=True)
