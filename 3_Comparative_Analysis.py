import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_and_clean_data, VEG_DATA_PATH, WEATHER_DATA_PATH

st.set_page_config(layout="wide")

# Load data (this will be cached by Streamlit)
df_veg, df_wea, df_combined = load_and_clean_data(VEG_DATA_PATH, WEATHER_DATA_PATH)

if df_combined is None:
    st.error("Data loading failed. Please check data files and paths in utils/data_loader.py.")
    st.stop()

# --- IMPORTANT: Ensure 'Year' and 'Month' are in df_wea for new charts ---
# This block is crucial if load_and_clean_data doesn't already add 'Year'/'Month' to df_wea
date_column_name_in_df_wea = 'Date' # <--- Verify this column name in your weather data

if not df_wea.empty and date_column_name_in_df_wea in df_wea.columns:
    df_wea[date_column_name_in_df_wea] = pd.to_datetime(df_wea[date_column_name_in_df_wea], errors='coerce')
    df_wea.dropna(subset=[date_column_name_in_df_wea], inplace=True)
    df_wea['Year'] = df_wea[date_column_name_in_df_wea].dt.year
    df_wea['Month'] = df_wea[date_column_name_in_df_wea].dt.month
else:
    st.warning(f"Weather data is empty or '{date_column_name_in_df_wea}' column not found in df_wea. Some weather analyses might be limited.")
# --- END IMPORTANT BLOCK ---

st.title("⚖️ Comparative Analysis")
st.markdown("Compare price trends and weather impacts across different crops or years.")

st.subheader("Price Comparison Across Vegetables")
# Allow selecting multiple vegetables for comparison
selected_vegetables_compare = st.sidebar.multiselect(
    "Select Vegetables to Compare (Price)",
    df_combined['Vegetable'].unique(),
    default=df_combined['Vegetable'].unique().tolist() # Default to all
)

if selected_vegetables_compare:
    df_compare = df_combined[df_combined['Vegetable'].isin(selected_vegetables_compare)].copy()
    
    # Ensure 'Date' is datetime and Year/Month are extracted for all relevant operations
    if 'Date' in df_compare.columns:
        df_compare['Date'] = pd.to_datetime(df_compare['Date'], errors='coerce')
        df_compare.dropna(subset=['Date'], inplace=True)
        df_compare['Year'] = df_compare['Date'].dt.year
        df_compare['Month'] = df_compare['Date'].dt.month

    # 1. Modal Price Distribution (Histogram)
    st.markdown("#### Modal Price Distribution (Histogram)")
    fig_compare_modal_price_hist = px.histogram(
        df_compare,
        x='Modal_Price',
        color='Vegetable', # Color by vegetable within facets
        facet_col='Vegetable', # Create separate columns for each vegetable
        facet_col_wrap=2, # Wrap columns for better layout
        title='Modal Price Distribution by Vegetable',
        labels={'Modal_Price': 'Modal Price (Rs./Quintal)', 'count': 'Frequency'},
        nbins=50, # Number of bins for the histogram
        opacity=0.8, # Add some transparency
        color_discrete_sequence=px.colors.qualitative.Bold # Vibrant palette
    )
    fig_compare_modal_price_hist.update_layout(height=500)
    fig_compare_modal_price_hist.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1])) # Clean facet titles
    st.plotly_chart(fig_compare_modal_price_hist, use_container_width=True)

    # 2. Minimum Price Distribution (Histogram)
    st.markdown("#### Minimum Price Distribution (Histogram)")
    fig_compare_min_price_hist = px.histogram(
        df_compare,
        x='Min_Price',
        color='Vegetable',
        facet_col='Vegetable',
        facet_col_wrap=2,
        title='Minimum Price Distribution by Vegetable',
        labels={'Min_Price': 'Minimum Price (Rs./Quintal)', 'count': 'Frequency'},
        nbins=50,
        opacity=0.8,
        color_discrete_sequence=px.colors.qualitative.Pastel # Pastel palette
    )
    fig_compare_min_price_hist.update_layout(height=500)
    fig_compare_min_price_hist.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig_compare_min_price_hist, use_container_width=True)

    # 3. Maximum Price Distribution (Histogram)
    st.markdown("#### Maximum Price Distribution (Histogram)")
    fig_compare_max_price_hist = px.histogram(
        df_compare,
        x='Max_Price',
        color='Vegetable',
        facet_col='Vegetable',
        facet_col_wrap=2,
        title='Maximum Price Distribution by Vegetable',
        labels={'Max_Price': 'Maximum Price (Rs./Quintal)', 'count': 'Frequency'},
        nbins=50,
        opacity=0.8,
        color_discrete_sequence=px.colors.sequential.Sunset # Muted/Earthy tones
    )
    fig_compare_max_price_hist.update_layout(height=500)
    fig_compare_max_price_hist.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig_compare_max_price_hist, use_container_width=True)
    
    # The original "Monthly Price Distribution (Box Plot)" is replaced by the above histograms
    # If you still wanted a monthly distribution specifically, we would adjust one of the histograms
    # or re-add a separate chart focusing on monthly aggregation.
    # For now, these three histograms cover the overall price distribution comparison.

else:
    st.info("Please select at least one vegetable to compare.")

st.subheader("Weather Comparison by Year")

# Allow selecting multiple years for weather comparison
selected_weather_years_compare = st.sidebar.multiselect(
    "Select Years to Compare (Weather)",
    sorted(df_wea['Year'].unique(), reverse=True), # Use 'Year' column created above
    default=sorted(df_wea['Year'].unique(), reverse=True)[:2] # Default to most recent two years
)

if selected_weather_years_compare and not df_wea.empty and 'Year' in df_wea.columns:
    df_weather_compare = df_wea[df_wea['Year'].isin(selected_weather_years_compare)]

    # 1. Average Temperature Trend Comparison by Year (Still a Line Graph, as trends are best shown by lines)
    st.markdown("#### Average Temperature Trends by Year")
    fig_temp_comp = px.line(
        df_weather_compare,
        x='Date',
        y='Avg_Temp_C',
        color='Year', # Color by Year
        title='Average Temperature Trends Comparison by Year',
        labels={'Avg_Temp_C': 'Average Temperature (°C)', 'Date': 'Date'},
        color_discrete_sequence=px.colors.qualitative.Dark24 # Another distinct qualitative palette
    )
    st.plotly_chart(fig_temp_comp, use_container_width=True)

    # 2. Precipitation Trend Comparison by Year (Still a Line Graph)
    st.markdown("#### Precipitation Trends by Year")
    fig_prcp_comp = px.line(
        df_weather_compare,
        x='Date',
        y='Precipitation_mm',
        color='Year', # Color by Year
        title='Precipitation Trends Comparison by Year',
        labels={'Precipitation_mm': 'Precipitation (mm)', 'Date': 'Date'},
        color_discrete_sequence=px.colors.qualitative.Light24 # Lighter distinct qualitative palette
    )
    st.plotly_chart(fig_prcp_comp, use_container_width=True)

    # 3. Monthly Average Weather Metrics Comparison (Bar Chart)
    st.markdown("#### Monthly Average Weather Metrics Comparison")
    weather_metric_compare = st.selectbox(
        "Select Weather Metric for Monthly Comparison",
        ['Avg_Temp_C', 'Min_Temp_C', 'Max_Temp_C', 'Precipitation_mm', 'Wind_Speed_kmh', 'Pressure_hPa']
    )

    monthly_weather_avg_comp = df_weather_compare.groupby(['Year', 'Month'])[weather_metric_compare].mean().reset_index()

    fig_monthly_weather_comp = px.bar(
        monthly_weather_avg_comp,
        x='Month',
        y=weather_metric_compare,
        color='Year',
        barmode='group', # Group bars by year for comparison
        title=f'Monthly Average {weather_metric_compare} Comparison by Year',
        labels={weather_metric_compare: weather_metric_compare, 'Month': 'Month'},
        color_discrete_sequence=px.colors.qualitative.G10 # A common 10-color palette
    )
    st.plotly_chart(fig_monthly_weather_comp, use_container_width=True)

    # 4. Weather Variable Correlation Heatmap
    st.markdown("#### Weather Variable Correlation Heatmap")
    # Select relevant numerical weather columns for correlation
    weather_cols_for_corr = [col for col in ['Avg_Temp_C', 'Min_Temp_C', 'Max_Temp_C', 'Precipitation_mm', 'Wind_Speed_kmh', 'Pressure_hPa'] if col in df_wea.columns]
    
    if weather_cols_for_corr:
        # Calculate correlation matrix
        # Ensure data is numeric for correlation
        corr_matrix = df_wea[weather_cols_for_corr].apply(pd.to_numeric, errors='coerce').corr()

        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True, # Show correlation values on heatmap
            aspect="auto", # Adjust aspect ratio
            color_continuous_scale=px.colors.sequential.RdBu, # Red-Blue diverging scale
            title='Correlation Heatmap of Weather Variables'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("Not enough numerical weather data for correlation heatmap.")


else:
    st.warning("No weather data available for the selected years or 'Year' column missing from df_wea.")