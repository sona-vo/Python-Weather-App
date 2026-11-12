# 🌦️ Python Weather App

## Project Overview
The Python Weather App is a simple application that provides real-time weather information for any city using the OpenWeatherMap API.

Users can enter a city name and get current weather details such as temperature, humidity, and weather conditions.

## Features
- Real-time weather information
- Search weather by city name
- Temperature displayed in Celsius
- Humidity information
- Weather condition description
- API integration
- Error handling for invalid cities
- Network and timeout error handling
- Option to check another city

## Technologies Used
- Python
- Requests
- OpenWeatherMap API
- Python-dotenv

## Project Structure
```text
Python-Weather-App/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

## Installation

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Navigate to the project folder:

```bash
cd Python-Weather-App
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Get an API key from OpenWeatherMap.

5. Create a `.env` file and add:

```text
API_KEY=your_api_key
```

6. Run the application:

```bash
python main.py
```

## Sample Output

```text
Enter A City: Calicut

Weather in Kozhikode, IN
------------------------------
Temperature : 29 °C
Humidity    : 75%
Conditions  : scattered clouds

Check another city? (y/n):
```

## Concepts Used
- Python Functions
- Conditional Statements
- While Loops
- Exception Handling
- API Integration
- JSON Data Handling
- Environment Variables
- User Input Handling

## Future Improvements
- Weather forecast for upcoming days
- Graphical User Interface (GUI)
- Weather icons
- Additional weather information

## Author
Sona V O

**GitHub:** https://github.com/sona-vo
