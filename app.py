from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_KEY = "5252d501f418435688c91350242301"  # Replace with your actual API key
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

@app.route("/")

def index():
    city_name =  "London"  # Use input city or default
    weather_data = get_weather_data(city_name)
    if weather_data["error"]:
        return render_template("error.html", error=weather_data["error"])
    return render_template("index.html", weather_data=weather_data)

def get_weather_data(city_name):
    url = f"{BASE_URL}?key={API_KEY}&q={city_name}&days=3"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["location"]["name"],
            "current": {
                "temperature": data["current"]["temp_c"],
               # "wind_speed": data["current"]["wind_speed"],  # Uncomment to include wind speed
                "condition": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["code"],
            },
            "forecast": data["forecast"]["forecastday"][:3],  # next 3 days
            "map_url": f"https://www.openstreetmap.org/?q={city_name}",
        }
    else:
        return {"error": "Cannot retrieve weather data"}

if __name__ == "__main__":
    app.run(debug=True)
