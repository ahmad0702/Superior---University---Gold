from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder="templates")

API_KEY = "ec277f3ce32236ba3c997164e841c3c5"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form["city"]
        params = {"q": city, "appid": API_KEY, "units": "metric"}

        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}.png"
            }
        else:
            weather_data = {"error": "City not found!"}

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
