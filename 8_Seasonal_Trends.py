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

# --- Data Preparation for Seasonal Analysis (Ensuring 'Year', 'Month', 'Day' columns) ---
date_column_name_in_df_wea = 'Date'

if not df_wea.empty and date_column_name_in_df_wea in df_wea.columns:
    df_wea[date_column_name_in_df_wea] = pd.to_datetime(df_wea[date_column_name_in_df_wea], errors='coerce')
    df_wea.dropna(subset=[date_column_name_in_df_wea], inplace=True)
    df_wea['Year'] = df_wea[date_column_name_in_df_wea].dt.year
    df_wea['Month'] = df_wea[date_column_name_in_df_wea].dt.month
else:
    st.warning(f"Weather data is empty or '{date_column_name_in_df_wea}' column not found in df_wea. Seasonal weather analysis might be limited.")

if 'Date' in df_combined.columns:
    df_combined['Date'] = pd.to_datetime(df_combined['Date'], errors='coerce')
    df_combined.dropna(subset=['Date'], inplace=True)
    df_combined['Year'] = df_combined['Date'].dt.year
    df_combined['Month'] = df_combined['Date'].dt.month
    df_combined['Day'] = df_combined['Date'].dt.day


st.title("📅 Seasonal Trends Analysis")
st.markdown("Examine how crop prices and weather patterns vary across different seasons and years in Hoshiarpur.")

# --- Monthly Average Prices Across Years (Modal Price) ---
st.subheader("Monthly Average Price Distributions Across Years")
selected_veg_seasonal = st.selectbox(
    "Select a Vegetable for Seasonal Price Analysis",
    df_combined['Vegetable'].unique(),
    key='selected_veg_seasonal_price'
)

df_seasonal_veg = df_combined[df_combined['Vegetable'] == selected_veg_seasonal]
if not df_seasonal_veg.empty:
    available_years_veg = sorted(df_seasonal_veg['Year'].unique())

    default_years_veg_display = available_years_veg[-5:] if len(available_years_veg) >= 5 else available_years_veg

    selected_years_veg_display = st.multiselect(
        f"Select Years to Display for {selected_veg_seasonal} Price Distributions",
        available_years_veg,
        default=default_years_veg_display,
        key='selected_years_veg_display'
    )

    if selected_years_veg_display:
        df_seasonal_veg_filtered = df_seasonal_veg[df_seasonal_veg['Year'].isin(selected_years_veg_display)].copy()

        # Group by Year and Month to get monthly averages for histogram
        monthly_avg_data = df_seasonal_veg_filtered.groupby(['Year', 'Month']).agg(
            Modal_Price=('Modal_Price', 'mean'),
            Min_Price=('Min_Price', 'mean'),
            Max_Price=('Max_Price', 'mean')
        ).reset_index()

        # NEW: Histogram for Monthly Average Modal Price
        st.markdown("#### Distribution of Monthly Average Modal Price")
        fig_monthly_avg_modal_hist = px.histogram(
            monthly_avg_data,
            x='Modal_Price',
            color='Year',
            barmode='overlay', # Overlay histograms for comparison
            title=f'Distribution of Monthly Average Modal Price for {selected_veg_seasonal}',
            labels={'Modal_Price': 'Average Modal Price (Rs./Quintal)', 'count': 'Frequency'},
            nbins=30, # Adjust number of bins as needed
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Alphabet # Vibrant palette
        )
        st.plotly_chart(fig_monthly_avg_modal_hist, use_container_width=True)

        # NEW: Histogram for Monthly Average Min Price
        st.markdown("#### Distribution of Monthly Average Minimum Price")
        fig_monthly_avg_min_hist = px.histogram(
            monthly_avg_data,
            x='Min_Price',
            color='Year',
            barmode='overlay',
            title=f'Distribution of Monthly Average Minimum Price for {selected_veg_seasonal}',
            labels={'Min_Price': 'Average Min Price (Rs./Quintal)', 'count': 'Frequency'},
            nbins=30,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Pastel # Pastel palette
        )
        st.plotly_chart(fig_monthly_avg_min_hist, use_container_width=True)

        # NEW: Histogram for Monthly Average Max Price
        st.markdown("#### Distribution of Monthly Average Maximum Price")
        fig_monthly_avg_max_hist = px.histogram(
            monthly_avg_data,
            x='Max_Price',
            color='Year',
            barmode='overlay',
            title=f'Distribution of Monthly Average Maximum Price for {selected_veg_seasonal}',
            labels={'Max_Price': 'Average Max Price (Rs./Quintal)', 'count': 'Frequency'},
            nbins=30,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Vivid # Another vibrant palette
        )
        st.plotly_chart(fig_monthly_avg_max_hist, use_container_width=True)

    else:
        st.info("Select years to view monthly average price distributions.")

else:
    st.info("No data for seasonal analysis for the selected vegetable.")

# --- Seasonal Weather Patterns (Histograms) ---
st.subheader("Seasonal Weather Patterns Distributions Across Years")
weather_metric = st.selectbox(
    "Select a Weather Metric for Seasonal Analysis",
    ['Avg_Temp_C', 'Precipitation_mm', 'Min_Temp_C', 'Max_Temp_C', 'Wind_Speed_kmh', 'Pressure_hPa'],
    key='weather_metric_seasonal'
)

if not df_wea.empty and 'Year' in df_wea.columns and 'Month' in df_wea.columns:
    available_years_wea = sorted(df_wea['Year'].unique())
    default_years_wea_display = available_years_wea[-5:] if len(available_years_wea) >= 5 else available_years_wea

    selected_years_wea_display = st.multiselect(
        f"Select Years to Display for {weather_metric} Distributions",
        available_years_wea,
        default=default_years_wea_display,
        key='selected_years_wea_display'
    )

    if selected_years_wea_display:
        df_wea_filtered = df_wea[df_wea['Year'].isin(selected_years_wea_display)].copy()

        # Group by Year and Month to get monthly averages for histogram
        monthly_weather_avg_data = df_wea_filtered.groupby(['Year', 'Month'])[weather_metric].mean().reset_index()

        # NEW: Histogram for Monthly Average Weather Metric
        fig_monthly_weather_hist = px.histogram(
            monthly_weather_avg_data,
            x=weather_metric,
            color='Year',
            barmode='overlay',
            title=f'Distribution of Monthly Average {weather_metric} Across Years',
            labels={weather_metric: weather_metric, 'count': 'Frequency'},
            nbins=30,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.G10 # Another distinct palette for weather
        )
        st.plotly_chart(fig_monthly_weather_hist, use_container_width=True)
    else:
        st.info("Select years to view monthly average weather distributions.")
else:
    st.info("No weather data available for seasonal analysis or 'Year'/'Month' columns could not be created.")

# --- NEW: Yearly Average Prices and Weather Summary Table ---
st.subheader("Yearly Average Prices and Weather Summary")

if not df_combined.empty and 'Year' in df_combined.columns:
    summary_cols = ['Modal_Price', 'Min_Price', 'Max_Price', 'Avg_Temp_C', 'Precipitation_mm']
    existing_summary_cols = [col for col in summary_cols if col in df_combined.columns]

    if existing_summary_cols:
        yearly_summary_data = df_combined.groupby(['Vegetable', 'Year'])[existing_summary_cols].mean().reset_index()
        yearly_summary_data.columns = ['Vegetable', 'Year'] + [f'Avg {col.replace("_", " ")}' for col in existing_summary_cols]
        st.dataframe(yearly_summary_data)
    else:
        st.info("Not enough data columns available for yearly summary.")
else:
    st.info("No combined data available for yearly summary or 'Year' column could not be created.")

# --- NEW: Price-Weather Correlation Heatmap (Overall) ---
st.subheader(f"Overall Price-Weather Correlation Heatmap")
st.markdown("Shows correlation between all vegetable prices and weather variables across all available data.")

correlation_cols_overall = [
    'Modal_Price', 'Min_Price', 'Max_Price',
    'Avg_Temp_C', 'Precipitation_mm', 'Min_Temp_C', 'Max_Temp_C',
    'Wind_Speed_kmh', 'Pressure_hPa'
]
correlation_cols_present_overall = [col for col in correlation_cols_overall if col in df_combined.columns]

if len(correlation_cols_present_overall) > 1 and not df_combined.empty:
    corr_df = df_combined[correlation_cols_present_overall].apply(pd.to_numeric, errors='coerce').dropna()
    if not corr_df.empty:
        corr_matrix = corr_df.corr()

        fig_heatmap_overall = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale=px.colors.sequential.Viridis,
            title='Overall Correlation Heatmap: All Vegetable Prices vs. Weather Variables'
        )
        fig_heatmap_overall.update_xaxes(side="top")
        st.plotly_chart(fig_heatmap_overall, use_container_width=True)
    else:
        st.info("Not enough valid numerical data to generate the overall correlation heatmap.")
else:
    st.info("Not enough data columns available to generate an overall correlation heatmap.")

# --- NEW: Price-Weather Correlation Heatmap (Selected Vegetable) ---
st.subheader(f"Price-Weather Correlation Heatmap for {selected_veg_seasonal}")
st.markdown(f"Shows correlation between {selected_veg_seasonal} prices and weather variables.")

if not df_seasonal_veg.empty:
    correlation_cols_veg = [
        'Modal_Price', 'Min_Price', 'Max_Price',
        'Avg_Temp_C', 'Precipitation_mm', 'Min_Temp_C', 'Max_Temp_C',
        'Wind_Speed_kmh', 'Pressure_hPa'
    ]
    correlation_cols_present_veg = [col for col in correlation_cols_veg if col in df_seasonal_veg.columns]

    if len(correlation_cols_present_veg) > 1:
        corr_df_veg = df_seasonal_veg[correlation_cols_present_veg].apply(pd.to_numeric, errors='coerce').dropna()
        if not corr_df_veg.empty:
            corr_matrix_veg = corr_df_veg.corr()

            fig_heatmap_veg = px.imshow(
                corr_matrix_veg,
                text_auto=True,
                aspect="auto",
                color_continuous_scale=px.colors.sequential.Plasma,
                title=f'Correlation Heatmap for {selected_veg_seasonal} Price and Weather Variables'
            )
            fig_heatmap_veg.update_xaxes(side="top")
            st.plotly_chart(fig_heatmap_veg, use_container_width=True)
        else:
            st.info(f"Not enough valid numerical data for {selected_veg_seasonal} to generate this correlation heatmap.")
    else:
        st.info(f"Not enough data columns available for {selected_veg_seasonal} to generate a correlation heatmap.")
else:
    st.info(f"No data available for {selected_veg_seasonal} to generate a correlation heatmap.")