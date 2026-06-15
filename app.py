import streamlit as st
import pandas as pd
import plotly.express as px

from components.metric_cards import metric_card

from services.weather_service import get_current_weather
from services.forecast_service import get_forecast

from components.charts import create_temperature_chart
from components.recommendations import get_recommendation

from services.aqi_service import get_aqi

from utils.favorites import (
    add_city,
    load_favorites
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="WeatherInsight Pro",
    page_icon="🌤",
    layout="wide"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🌤 WeatherInsight Pro")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Forecast",
        "Favorites",
        "AQI",
        "Compare Cities",
        "About"
    ]
)

# =====================================
# DASHBOARD
# =====================================

if page == "Dashboard":

    st.title("🌤 WeatherInsight Pro")

    city = st.text_input(
        "Enter City Name",
        value="Hyderabad"
    )

    col_a, col_b = st.columns([4, 1])

    with col_b:
        if st.button("⭐ Save City"):
            add_city(city)
            st.success(
                f"{city} saved"
            )

    if st.button("Get Weather"):

        weather = get_current_weather(city)
        forecast = get_forecast(city)

        if weather:

            temp = weather["main"]["temp"]
            humidity = weather["main"]["humidity"]
            wind = weather["wind"]["speed"]

            feels_like = weather["main"]["feels_like"]
            pressure = weather["main"]["pressure"]
            visibility = weather.get(
                "visibility",
                0
            ) / 1000

            condition = weather["weather"][0]["description"]

            icon_code = weather["weather"][0]["icon"]

            icon_url = (
                f"https://openweathermap.org/img/wn/"
                f"{icon_code}@4x.png"
            )

            # =====================
            # METRIC CARDS
            # =====================

            col1, col2, col3 = st.columns(3)

            with col1:
                metric_card(
                    "Temperature",
                    f"{temp:.1f} °C",
                    "🌡"
                )

            with col2:
                metric_card(
                    "Humidity",
                    f"{humidity}%",
                    "💧"
                )

            with col3:
                metric_card(
                    "Wind Speed",
                    f"{wind:.1f} m/s",
                    "🌬"
                )

            col4, col5, col6 = st.columns(3)

            with col4:
                metric_card(
                    "Feels Like",
                    f"{feels_like:.1f} °C",
                    "🤗"
                )

            with col5:
                metric_card(
                    "Pressure",
                    f"{pressure} hPa",
                    "📊"
                )

            with col6:
                metric_card(
                    "Visibility",
                    f"{visibility:.1f} km",
                    "👁"
                )

            st.divider()

            # =====================
            # WEATHER CONDITION
            # =====================

            st.subheader("Weather Condition")

            col7, col8 = st.columns([1, 4])

            with col7:
                st.image(
                    icon_url,
                    width=120
                )

            with col8:
                st.markdown(
                    f"## {condition.title()}"
                )

            st.divider()

            # =====================
            # RECOMMENDATION
            # =====================

            st.subheader(
                "Recommendation"
            )

            st.success(
                get_recommendation(
                    temp,
                    condition
                )
            )

            st.divider()

            # =====================
            # QUICK FORECAST
            # =====================

            if forecast:

                st.subheader(
                    "Temperature Forecast"
                )

                fig = create_temperature_chart(
                    forecast
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.error(
                "City not found"
            )

# =====================================
# FORECAST PAGE
# =====================================

if page == "Forecast":

    st.title("📈 Forecast")

    city = st.text_input(
        "Forecast City",
        value="Hyderabad"
    )

    if st.button("Get Forecast"):

        forecast = get_forecast(city)

        if forecast:

            st.success(
                f"Forecast loaded for {city}"
            )

            fig = create_temperature_chart(
                forecast
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.error(
                "Forecast unavailable"
            )

# =====================================
# FAVORITES PAGE
# =====================================

if page == "Favorites":

    st.title("⭐ Favorite Cities")

    favorites = load_favorites()

    if favorites["cities"]:

        for city in favorites["cities"]:

            st.write(
                f"📍 {city}"
            )

    else:

        st.warning(
            "No favorite cities saved."
        )

# =====================================
# AQI PAGE
# =====================================

if page == "AQI":

    st.title("🌫 Air Quality Index")

    city = st.text_input(
        "Enter City",
        value="Hyderabad",
        key="aqi_city"
    )

    if st.button(
        "Get AQI"
    ):

        weather = get_current_weather(city)

        if weather:

            lat = weather["coord"]["lat"]
            lon = weather["coord"]["lon"]

            aqi_data = get_aqi(
                lat,
                lon
            )

            if aqi_data:

                data = aqi_data["list"][0]

                aqi = data["main"]["aqi"]

                components = data[
                    "components"
                ]

                st.subheader(
                    f"Air Quality Level: {aqi}"
                )

                if aqi == 1:
                    st.success(
                        "Good Air Quality"
                    )

                elif aqi == 2:
                    st.info(
                        "Fair Air Quality"
                    )

                elif aqi == 3:
                    st.warning(
                        "Moderate Air Quality"
                    )

                else:
                    st.error(
                        "Poor Air Quality"
                    )

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "PM2.5",
                        components["pm2_5"]
                    )

                    st.metric(
                        "PM10",
                        components["pm10"]
                    )

                with col2:
                    st.metric(
                        "CO",
                        components["co"]
                    )

                    st.metric(
                        "NO₂",
                        components["no2"]
                    )

        else:

            st.error(
                "City not found"
            )
# =====================================
# COMPARE CITIES PAGE
# =====================================

if page == "Compare Cities":
    st.title("🏙 Compare Cities")

    col1, col2 = st.columns(2)

    with col1:
        city1 = st.text_input(
            "City 1",
            value="Hyderabad",
            key="city1"
        )

    with col2:
        city2 = st.text_input(
            "City 2",
            value="Bangalore",
            key="city2"
        )

    if st.button("Compare Cities"):
        weather1 = get_current_weather(city1)
        weather2 = get_current_weather(city2)

        if weather1 and weather2:
            comparison_data = {
                "Metric": [
                    "Temperature",
                    "Humidity",
                    "Wind Speed",
                    "Pressure"
                ],
                city1: [
                    weather1["main"]["temp"],
                    weather1["main"]["humidity"],
                    weather1["wind"]["speed"],
                    weather1["main"]["pressure"]
                ],
                city2: [
                    weather2["main"]["temp"],
                    weather2["main"]["humidity"],
                    weather2["wind"]["speed"],
                    weather2["main"]["pressure"]
                ]
            }

            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)

            chart_df = pd.DataFrame({
                "City": [city1, city2],
                "Temperature": [
                    weather1["main"]["temp"],
                    weather2["main"]["temp"]
                ]
            })

            fig = px.bar(
                chart_df,
                x="City",
                y="Temperature",
                title="Temperature Comparison"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Unable to fetch weather data.")

# =====================================
# ABOUT PAGE
# =====================================

if page == "About":
    st.title("ℹ About")

    st.write(
        """

# WeatherInsight Pro

Advanced Weather Dashboard

### Technologies

- Python
- Streamlit
- Requests
- OpenWeatherMap API
- Plotly

### Features

- Real-time weather
- Forecast charts
- Favorites
- Recommendations
- Modern UI

# Developed by :Jafar Hussain Galibaigari
# Mail: jafar3760409@gmail.com
# Contact No: +91 6309308147
        """
    )
    