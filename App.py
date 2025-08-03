import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

classification_model = pickle.load(open("road_accident_classification.sav", "rb"))
time_series_models = pickle.load(open("severity_arima_models.sav", "rb"))

st.set_page_config(page_title="Road Accident Prediction", layout="wide")
st.title("🚦 Road Accident Prediction System")

col1, col2 = st.columns(2)

with col1:
    st.header("📊 Accident Severity Classification")
    month = st.selectbox("Month", list(range(1, 13)))
    day_of_week = st.selectbox("Day of Week", list(range(1, 8)))
    year = st.number_input("Year", min_value=2000, max_value=2100, value=2023)
    junction_control = st.selectbox("Junction Control", [0, 1, 2, 3])
    junction_detail = st.selectbox("Junction Detail", [0, 1, 2, 3])
    latitude = st.number_input("Latitude", value=51.5)
    longitude = st.number_input("Longitude", value=-0.1)
    speed_limit = st.number_input("Speed limit", value=30)
    number_of_vehicles = st.number_input("Number of Vehicles", min_value=1, value=1)
    light_conditions = st.selectbox("Light Conditions", [0, 1, 2, 3])
    local_authority = st.selectbox("Local Authority (District)", [0, 1, 2, 3])
    number_of_casualties = st.number_input("Number of Casualties", min_value=0, value=0)
    police_force = st.selectbox("Police Force", [0, 1, 2, 3])
    road_surface = st.selectbox("Road Surface Conditions", [0, 1, 2])
    road_type = st.selectbox("Road Type", [0, 1, 2])
    weather = st.selectbox("Weather Conditions", [0, 1, 2, 3])
    vehicle_type = st.selectbox("Vehicle Type", [0, 1, 2, 3])
    is_night = st.selectbox("Is Night", [0, 1])
    bad_weather = st.selectbox("Bad Weather", [0, 1])

    urban_rural = st.selectbox("Urban or Rural Area", [0, 1])
hour = st.slider("Hour", 0, 23, 12)
minute = st.slider("Minute", 0, 59, 0)

if st.button("🚗 Predict Severity"):
    input_data = np.array([[month, day_of_week, year, junction_control, junction_detail,
                            latitude, light_conditions, local_authority, longitude,
                            number_of_casualties, number_of_vehicles, police_force,
                            road_surface, road_type, speed_limit, weather, vehicle_type,
                            urban_rural, hour, is_night, bad_weather, minute]])
    
    prediction = classification_model.predict(input_data)[0]
    result = "⚠️ High Risk Accident" if prediction == 1 else "✅ Low Risk Accident"
    st.success(f"Prediction: {result}")


with col2:
    st.header("⏳ Accident Forecast (Time Series)")
    steps = st.slider("Number of months to forecast:", 1, 12, 5)

    if st.button("📈 Forecast by Severity Levels"):
        for severity, model in time_series_models.items():
            forecast = model.get_forecast(steps=steps)
            forecast_values = forecast.predicted_mean
            forecast_index = pd.date_range(model.data.dates[-1], periods=steps+1, freq='M')[1:]
            
            st.subheader(f"Severity: **{severity}**")
            forecast_df = pd.DataFrame({
                "Date": forecast_index,
                "Forecasted Accidents": forecast_values.values
            })
            st.dataframe(forecast_df)

            fig, ax = plt.subplots()
            ax.plot(forecast_index, forecast_values, marker='o', label='Forecast')
            ax.set_title(f"Accident Forecast for {severity}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Accident Count")
            ax.grid(True)
            st.pyplot(fig)
