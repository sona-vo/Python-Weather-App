import os, sys, requests
from dotenv import load_dotenv

load_dotenv()                        # reads the .env file into environment variables
API_KEY = os.getenv("API_KEY")       # returns None if the key isn't set
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

if not API_KEY:
    print("Error: API key not found.")
    print("Create a .env file containing: API_KEY=your_key_here")
    sys.exit(1)                      # stops the program
    
def get_city():
    city = input('Enter A City:').strip()
    while not city:
        city = input("Invalid! Try Again:").strip()
    return city
    
def fetch_weather(city, api_key):
    params = {
        "q": city,          # city name typed by the user
        "appid": api_key,   # your API key
        "units": "metric",  # Celsius instead of Kelvin
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Network error: check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong with the request: {e}")
        return None
    if response.status_code == 404:
        print(f"City '{city}' not found. Check the spelling and try again.")
        return None
    elif response.status_code == 401:
        print('Invalid API key. Check your .env file.')
        return None
    try:
        response.raise_for_status()   # raises an error for any other bad status
        return response.json()        # runs only if there was no error
    except requests.exceptions.HTTPError as e:
        print(f"Server error: {e}")
        return None
    except ValueError:
        print("Could not read the server's response.")
        return None

def display_weather(response):
    # .get() with a default avoids a crash if a field is missing
    city = response.get('name','Unknown')
    country = response.get('sys',{}).get('country','')
    temperature = response.get('main',{}).get('temp','N/A')
    humidity = response.get('main',{}).get('humidity','N/A')
    weather = response.get('weather') or [{}]
    condition = weather[0].get('description', 'N/A')
    print(f"Weather in {city}, {country}")
    print("-" * 30)
    print(f"Temperature : {temperature} °C")
    print(f"Humidity    : {humidity}%")
    print(f"Conditions  : {condition}")
    
def main():
    while True:
        city = get_city()
        data = fetch_weather(city, API_KEY)
        if data:
            display_weather(data)
        again = input("\nCheck another city? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()