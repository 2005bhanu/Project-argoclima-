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

st.title("🌶️ Capsicum Price & Weather Analysis")
st.markdown("Explore the relationship between Capsicum prices and weather conditions in Hoshiarpur.")

selected_vegetable = "Capsicum" # Hardcode for this page
df_selected_veg = df_combined[df_combined['Vegetable'] == selected_vegetable]

# --- Ensure Year and Month columns exist in df_selected_veg ---
if 'Date' in df_selected_veg.columns:
    df_selected_veg['Date'] = pd.to_datetime(df_selected_veg['Date'], errors='coerce')
    df_selected_veg.dropna(subset=['Date'], inplace=True)
    df_selected_veg['Year'] = df_selected_veg['Date'].dt.year
    df_selected_veg['Month'] = df_selected_veg['Date'].dt.month
    df_selected_veg['Day'] = df_selected_veg['Date'].dt.day # Also extract day for daily plots

if not df_selected_veg.empty:
    st.subheader(f"Price Distribution for {selected_vegetable}")

    # NEW: Histogram for Overall Modal Price Distribution (Vibrant)
    st.markdown("#### Overall Modal Price Distribution")
    fig_modal_price_hist = px.histogram(
        df_selected_veg,
        x='Modal_Price',
        title=f'Overall Modal Price Distribution for {selected_vegetable}',
        labels={'Modal_Price': 'Modal Price (Rs./Quintal)', 'count': 'Frequency'},
        nbins=50, # Adjust number of bins as needed
        color_discrete_sequence=['#FF6347'], # Vibrant Tomato color
        opacity=0.8
    )
    st.plotly_chart(fig_modal_price_hist, use_container_width=True)

    # NEW: Histogram for Overall Min Price Distribution (Pastel)
    st.markdown("#### Overall Minimum Price Distribution")
    fig_min_price_hist = px.histogram(
        df_selected_veg,
        x='Min_Price',
        title=f'Overall Minimum Price Distribution for {selected_vegetable}',
        labels={'Min_Price': 'Minimum Price (Rs./Quintal)', 'count': 'Frequency'},
        nbins=50,
        color_discrete_sequence=['#A2D2FF'], # Pastel Light Blue
        opacity=0.8
    )
    st.plotly_chart(fig_min_price_hist, use_container_width=True)

    # NEW: Histogram for Overall Max Price Distribution (Vibrant)
    st.markdown("#### Overall Maximum Price Distribution")
    fig_max_price_hist = px.histogram(
        df_selected_veg,
        x='Max_Price',
        title=f'Overall Maximum Price Distribution for {selected_vegetable}',
        labels={'Max_Price': 'Maximum Price (Rs./Quintal)', 'count': 'Frequency'},
        nbins=50,
        color_discrete_sequence=['#90EE90'], # Vibrant Light Green
        opacity=0.8
    )
    st.plotly_chart(fig_max_price_hist, use_container_width=True)


    # --- Year-over-Year Price Distribution Comparison (Histograms) ---
    st.subheader(f"Year-over-Year Price Distribution Comparison for {selected_vegetable}")

    available_years = sorted(df_selected_veg['Year'].unique())

    # Dynamically select available years, if less than 5, just pick all available
    years_to_compare = []
    if len(available_years) >= 5:
        years_to_compare = available_years[-5:]
    else:
        years_to_compare = available_years

    selected_years_yoy = st.multiselect(
        f"Select Years to Compare Price Distributions for {selected_vegetable}",
        available_years,
        default=years_to_compare,
        key=f'yoy_multiselect_{selected_vegetable}' # Unique key to prevent widget re-rendering issues
    )

    if selected_years_yoy:
        df_yoy = df_selected_veg[df_selected_veg['Year'].isin(selected_years_yoy)].copy()

        # Histogram for Year-over-Year Modal Price Distribution
        st.markdown("#### Year-over-Year Modal Price Distribution")
        fig_yoy_modal_hist = px.histogram(
            df_yoy,
            x='Modal_Price',
            color='Year', # Color bars by year
            barmode='overlay', # Overlay histograms for comparison
            title=f'Year-over-Year Modal Price Distribution for {selected_vegetable}',
            labels={'Modal_Price': 'Modal Price (Rs./Quintal)', 'count': 'Frequency'},
            nbins=50,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Set1 # A strong, distinct palette
        )
        st.plotly_chart(fig_yoy_modal_hist, use_container_width=True)

        # Histogram for Year-over-Year Min Price Distribution
        st.markdown("#### Year-over-Year Minimum Price Distribution")
        fig_yoy_min_hist = px.histogram(
            df_yoy,
            x='Min_Price',
            color='Year',
            barmode='overlay',
            title=f'Year-over-Year Minimum Price Distribution for {selected_vegetable}',
            labels={'Min_Price': 'Minimum Price (Rs./Quintal)', 'count': 'Frequency'},
            nbins=50,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Pastel1 # A softer pastel palette
        )
        st.plotly_chart(fig_yoy_min_hist, use_container_width=True)

        # Histogram for Year-over-Year Max Price Distribution
        st.markdown("#### Year-over-Year Maximum Price Distribution")
        fig_yoy_max_hist = px.histogram(
            df_yoy,
            x='Max_Price',
            color='Year',
            barmode='overlay',
            title=f'Year-over-Year Maximum Price Distribution for {selected_vegetable}',
            labels={'Max_Price': 'Maximum Price (Rs./Quintal)', 'count': 'Frequency'},
            nbins=50,
            opacity=0.7,
            color_discrete_sequence=px.colors.qualitative.Dark24 # Another distinct dark palette
        )
        st.plotly_chart(fig_yoy_max_hist, use_container_width=True)
    else:
        st.info("Select years to view year-over-year price distributions.")


    st.subheader(f"Correlation between {selected_vegetable} Price and Weather")
    col_temp, col_prcp = st.columns(2)
    with col_temp:
        fig_scatter_temp = px.scatter(
            df_selected_veg,
            x='Avg_Temp_C',
            y='Modal_Price',
            title=f'Modal Price vs. Average Temperature for {selected_vegetable}',
            labels={'Avg_Temp_C': 'Average Temperature (°C)', 'Modal_Price': 'Modal Price (Rs./Quintal)'},
            hover_data=['Date', 'Precipitation_mm'],
            color_discrete_sequence=['#32CD32'] # Lime Green (vibrant)
        )
        fig_scatter_temp.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_scatter_temp, use_container_width=True)
    with col_prcp:
        fig_scatter_prcp = px.scatter(
            df_selected_veg,
            x='Precipitation_mm',
            y='Modal_Price',
            title=f'Modal Price vs. Precipitation for {selected_vegetable}',
            labels={'Precipitation_mm': 'Precipitation (mm)', 'Modal_Price': 'Modal Price (Rs./Quintal)'},
            hover_data=['Date', 'Avg_Temp_C'],
            color_discrete_sequence=['#9370DB'] # Medium Purple (vibrant)
        )
        fig_scatter_prcp.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_scatter_prcp, use_container_width=True)

    st.subheader(f"Seasonal Price Variation for {selected_vegetable}")
    fig_seasonal = px.box(
        df_selected_veg,
        x='Month',
        y='Modal_Price',
        title=f'Monthly Price Distribution for {selected_vegetable}',
        labels={'Month': 'Month', 'Modal_Price': 'Modal Price (Rs./Quintal)'},
        points="all",
        color='Month', # Color each box based on the month
        color_discrete_sequence=px.colors.qualitative.Pastel2 # A different pastel palette
    )
    fig_seasonal.update_layout(xaxis_title="Month", yaxis_title="Modal Price (Rs./Quintal)")
    st.plotly_chart(fig_seasonal, use_container_width=True)

    # --- Monthly Average Price Bar Chart ---
    st.subheader(f"Monthly Average Modal Price Bar Chart for {selected_vegetable}")

    monthly_avg_price = df_selected_veg.groupby(['Year', 'Month'])['Modal_Price'].mean().reset_index()

    fig_bar_monthly_avg = px.bar(
        monthly_avg_price,
        x='Month',
        y='Modal_Price',
        color='Year', # Color bars by year
        barmode='group', # Group bars side-by-side for each month
        title=f'Monthly Average Modal Price for {selected_vegetable} by Year',
        labels={'Modal_Price': 'Average Modal Price (Rs./Quintal)', 'Month': 'Month'},
        color_discrete_sequence=px.colors.qualitative.T10 # Another vibrant qualitative palette
    )
    fig_bar_monthly_avg.update_layout(xaxis_title="Month", yaxis_title="Average Modal Price (Rs./Quintal)")
    st.plotly_chart(fig_bar_monthly_avg, use_container_width=True)

    # --- NEW: Price-Weather Correlation Heatmap ---
    st.subheader(f"Correlation Heatmap: {selected_vegetable} Price vs. Weather")

    correlation_cols = [
        'Modal_Price', 'Min_Price', 'Max_Price',
        'Avg_Temp_C', 'Precipitation_mm', 'Min_Temp_C', 'Max_Temp_C',
        'Wind_Speed_kmh', 'Pressure_hPa'
    ]
    correlation_cols_present = [col for col in correlation_cols if col in df_selected_veg.columns]

    if len(correlation_cols_present) > 1:
        corr_df = df_selected_veg[correlation_cols_present].apply(pd.to_numeric, errors='coerce').dropna()
        
        if not corr_df.empty:
            corr_matrix = corr_df.corr()

            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale=px.colors.sequential.RdBu,
                title=f'Correlation Heatmap for {selected_vegetable} Price and Weather Variables'
            )
            fig_heatmap.update_xaxes(side="top")
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info(f"Not enough valid numerical data for {selected_vegetable} to generate a correlation heatmap.")
    else:
        st.info(f"Not enough data columns available for {selected_vegetable} to generate a correlation heatmap.")

else:
    st.warning(f"No data available for {selected_vegetable}.")