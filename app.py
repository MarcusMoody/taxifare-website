import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🚖 TaxiFareModel front")
st.markdown("### Enter ride details to get a fare prediction")

# 1. Input fields
pickup_date = st.date_input("Pickup date", value=datetime.today())
pickup_time = st.time_input("Pickup time", value=datetime.now().time())
pickup_datetime = f"{pickup_date} {pickup_time}"

pickup_longitude = st.number_input("Pickup longitude", value=-73.985664)
pickup_latitude = st.number_input("Pickup latitude", value=40.748514)
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985135)
dropoff_latitude = st.number_input("Dropoff latitude", value=40.758984)
passenger_count = st.number_input("Passenger count", min_value=1, max_value=6, value=1)

# 2. Show map
st.markdown("### Ride Route Map")
map_data = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude]
})
st.map(map_data)

# 3. API URL
url = 'https://taxifare.lewagon.ai/predict'

# 4. Prediction
if st.button("Get fare prediction"):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json()
        fare = prediction.get("fare", "N/A")
        st.success(f"💰 Estimated fare: ${fare:.2f}")
    else:
        st.error("⚠️ API request failed. Please try again later.")
