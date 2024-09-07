import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit import header

st.title ("WeatherView")
# Add a file uploader to load the CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# Define required columns for the app
required_columns = ['timestamp', 'city_name', 'temperature', 'humidity', 'dew_point', 'wind_speed', 'cloudiness', 'uv_index', 'rain_volume', 'snow_volume']

if uploaded_file is not None:
    try:
        # Read the CSV file
        weather_data = pd.read_csv(uploaded_file)

        # Check if the required columns are in the uploaded file
        missing_columns = [col for col in required_columns if col not in weather_data.columns]
        if missing_columns:
            st.error(f"The following required columns are missing: {', '.join(missing_columns)}")
        else:
            # Convert timestamp to datetime for filtering
            weather_data['timestamp'] = pd.to_datetime(weather_data['timestamp'])

            # Sidebar for filters
            st.sidebar.header("Filter Options")
            cities = st.sidebar.multiselect('Select Cities', options=weather_data['city_name'].unique(), default=weather_data['city_name'].unique())
            time_range = st.sidebar.slider("Select Time Range",
                                           min_value=weather_data['timestamp'].min().to_pydatetime(),
                                           max_value=weather_data['timestamp'].max().to_pydatetime(),
                                           value=(weather_data['timestamp'].min().to_pydatetime(), weather_data['timestamp'].max().to_pydatetime()))

            # Apply filters
            filtered_data = weather_data[(weather_data['city_name'].isin(cities)) & (weather_data['timestamp'] >= time_range[0]) & (weather_data['timestamp'] <= time_range[1])]

            # Header for app
            st.header("Explore Weather Data by City")

            # Temperature Line Chart
            st.subheader("Temperature Comparison Across Cities")
            temp_chart = px.line(filtered_data, x='timestamp', y='temperature', color='city_name', labels={'temperature': 'Temperature (°F)'}, title="Temperature Over Time")
            st.plotly_chart(temp_chart)

            # Humidity vs Dew Point Scatter Plot
            st.subheader("Humidity vs Dew Point")
            humidity_dewpoint_chart = px.scatter(filtered_data, x='humidity', y='dew_point', color='city_name', labels={'humidity': 'Humidity (%)', 'dew_point': 'Dew Point (°F)'}, title="Humidity vs Dew Point")
            st.plotly_chart(humidity_dewpoint_chart)

            # Wind Speed and Cloudiness Bar Chart
            st.subheader("Wind Speed and Cloudiness")
            wind_cloudiness_chart = px.bar(filtered_data, x='timestamp', y=['wind_speed', 'cloudiness'], barmode='group', labels={'value': 'Value', 'timestamp': 'Time'}, title="Wind Speed and Cloudiness Over Time")
            st.plotly_chart(wind_cloudiness_chart)

            # UV Index Area Chart
            st.subheader("UV Index Over Time")
            uv_chart = px.area(filtered_data, x='timestamp', y='uv_index', color='city_name', labels={'uv_index': 'UV Index'}, title="UV Index Over Time")
            st.plotly_chart(uv_chart)

            # Rain/Precipitation Volume Bar Chart
            st.subheader("Precipitation (Rain/Snow) Volume")
            precipitation_chart = px.bar(filtered_data, x='timestamp', y=['rain_volume', 'snow_volume'], labels={'value': 'Volume (mm)', 'timestamp': 'Time'}, title="Rain and Snow Volume Over Time")
            st.plotly_chart(precipitation_chart)
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.write("Please upload a CSV file to get started.")
