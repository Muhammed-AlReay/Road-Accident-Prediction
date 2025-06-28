import streamlit as st
import pickle
import numpy as np

# تحميل النموذج المدرب
model = pickle.load(open("road_accident_model.sav", "rb"))

# عنوان التطبيق
st.title("🚦 Road Accident Risk Prediction")

st.markdown("This app predicts the **risk level** of road accidents based on input conditions.")

# إدخال البيانات من المستخدم
temperature = st.number_input("🌡️ Temperature (°C)", min_value=-20.0, max_value=50.0, value=25.0)
visibility = st.number_input("🌫️ Visibility (miles)", min_value=0.0, max_value=10.0, value=5.0)
weather = st.selectbox("⛅ Weather Condition", ['Clear', 'Rain', 'Snow', 'Fog'])

# ترميز حالة الطقس
weather_map = {'Clear': 0, 'Rain': 1, 'Snow': 2, 'Fog': 3}
weather_encoded = weather_map[weather]

# زر التنبؤ
if st.button("🚗 Predict Accident Risk"):
    input_data = np.array([[temperature, visibility, weather_encoded]])
    prediction = model.predict(input_data)[0]
    result = "⚠️ High Risk" if prediction == 1 else "✅ Low Risk"
    st.success(f"Prediction: {result}")
