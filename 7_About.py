import streamlit as st

st.set_page_config(layout="wide")

st.title("ℹ️ About This Project")
st.markdown("""
This Streamlit application is designed to analyze crop sales data for Capsicum, Carrot, and Potato in Hoshiarpur,
Punjab, India, in conjunction with local weather data over a 5-year period.

**Objective:**
* Identify trends in crop prices.
* Explore correlations between weather parameters (temperature, precipitation, wind, pressure) and crop prices.
* Provide insights into seasonal variations and potential impacts of climate on agriculture.

**Data Sources:**
* **Crop Sales Data:** Merged dataset of Capsicum, Carrot, and Potato prices (Min, Max, Modal) with dates.
* **Weather Data:** Daily weather parameters for Hoshiarpur (Average Temperature, Min/Max Temperature, Precipitation, Wind Speed, Pressure).

**Features:**
* **Overview Dashboard:** High-level summaries and overall trends.
* **Crop-Specific Analysis:** Detailed insights for individual crops, including price trends, weather correlations, and seasonal variations.
* **Comparative Analysis:** Compare price trends across multiple crops and analyze weather patterns by year.
* **[Crop Name] Weather Comparison:** Dedicated pages for detailed analysis of each specific crop's price against weather.
* **Seasonal Trends:** Deeper dive into seasonal patterns.

**Developed by:** Your Name/Team Name (Replace with your details)
**Date:** July 22, 2025 (Adjust as needed)
""")
