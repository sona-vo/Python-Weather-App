import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # reads the .env file into environment variables

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_api_key():
    """Look for the key in .env / environment first, then in Streamlit secrets."""
    key = os.getenv("API_KEY")
    if key:
        return key
    try:
        return st.secrets["API_KEY"]
    except Exception:
        return None


@st.cache_data(ttl=600, show_spinner=False)  # cache each city for 10 minutes
def fetch_weather(city, api_key):
    """Returns (data, error_message). Exactly one of them is None."""
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.Timeout:  # keep before ConnectionError
        return None, "The request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Network error: check your internet connection."
    except requests.exceptions.RequestException as e:
        return None, f"Something went wrong with the request: {e}"

    if response.status_code == 404:
        return None, f"City '{city}' not found. Check the spelling and try again."
    if response.status_code == 401:
        return None, "Invalid API key. New keys can take a couple of hours to activate."
    if response.status_code == 429:
        return None, "Rate limit reached. Please wait a bit and try again."

    try:
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        return None, f"Server error: {e}"
    except ValueError:
        return None, "Could not read the server's response."


def display_weather(data):
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather = data.get("weather") or [{}]
    condition = weather[0].get("description", "N/A").title()
    icon = weather[0].get("icon")

    location = f"{city}, {country}" if country else city
    st.subheader(f"Weather in {location}")

    col_icon, col_cond = st.columns([1, 4])
    if icon:
        col_icon.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=80)
    col_cond.markdown(f"### {condition}")

    temp = main.get("temp")
    feels = main.get("feels_like")
    humidity = main.get("humidity")
    wind_speed = wind.get("speed")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{temp:.1f} °C" if temp is not None else "N/A")
    c2.metric("Feels like", f"{feels:.1f} °C" if feels is not None else "N/A")
    c3.metric("Humidity", f"{humidity}%" if humidity is not None else "N/A")
    c4.metric("Wind", f"{wind_speed} m/s" if wind_speed is not None else "N/A")


def main():
    st.set_page_config(page_title="Weather App", page_icon="🌤️")
    st.title("🌤️ Weather App")

    api_key = get_api_key()
    if not api_key:
        st.error("API key not found.")
        st.markdown(
            "Create a `.env` file next to this script containing:\n\n"
            "```\nAPI_KEY=your_key_here\n```\n"
            "or add `API_KEY` to `.streamlit/secrets.toml`."
        )
        st.stop()

    with st.form("weather_form"):
        city = st.text_input("Enter a city", placeholder="e.g. Kochi")
        submitted = st.form_submit_button("Get weather")

    if submitted:
        city = city.strip()
        if not city:
            st.warning("Please enter a city name.")
            return

        with st.spinner("Fetching weather..."):
            data, error = fetch_weather(city, api_key)

        if error:
            st.error(error)
        else:
            display_weather(data)


if __name__ == "__main__":
    main()
