from datetime import datetime, timedelta
from meteostat import Point, Daily
import pandas as pd

# 1. Define Hoshiarpur's Coordinates
# Approximate coordinates for Hoshiarpur, Punjab, India:
# Latitude: 31.5322° N
# Longitude: 75.9172° E
# Altitude (optional, but good for accuracy if known, in meters): ~296 meters
location = Point(31.5322, 75.9172, 296) 

# 2. Define the Time Period (5 years)
end_date = datetime.now()
start_date = end_date - timedelta(days=5 * 365) # Get data for approximately 5 years

# Meteostat's Daily class requires datetime objects for start and end
start_date_daily = datetime(start_date.year, start_date.month, start_date.day)
end_date_daily = datetime(end_date.year, end_date.month, end_date.day)

print(f"Fetching daily weather data for Hoshiarpur from {start_date_daily.strftime('%Y-%m-%d')} to {end_date_daily.strftime('%Y-%m-%d')}")

# 3. Fetch the Daily Data
try:
    data = Daily(location, start_date_daily, end_date_daily)
    data = data.fetch()

    if data is not None and not data.empty:
        print("\nSuccessfully fetched data!")
        print("First 5 rows of the DataFrame:")
        print(data.head())

        print(f"\nLast 5 rows of the DataFrame (up to {end_date.strftime('%Y-%m-%d')}):")
        print(data.tail())

        # 4. Define the output filename
        output_filename = "hoshiarpur_weather_5_years.csv"
        
        # 5. Save the data to a CSV file
        # The 'index=False' argument prevents Pandas from writing the DataFrame index
        # as a separate column in the CSV file, which is usually desired.
        data.to_csv(output_filename, index=False) 
        print(f"\nData successfully saved to {output_filename}")

        # Basic data summary for verification
        print("\nData Summary:")
        print(data.info())
        print("\nDescriptive Statistics:")
        print(data.describe())

    else:
        print("No historical weather data found for Hoshiarpur within the specified period.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure your internet connection is stable and the Meteostat service is available.")
    print("You might also want to double-check the coordinates for Hoshiarpur.")