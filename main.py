import requests
import json
import configparser
from flask import Flask, render_template, request, send_from_directory, url_for

app = Flask(__name__)

#gets API key from config
def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["weatherUI"]["api"]

#handles the SEO
@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/", methods= ['GET', 'POST'])
def index():

    #checks if user has submitted the form
    if request.method == "POST":

        #gets data from user form
        city_name = request.form["city"]
        country_name = request.form["country"]

        #stores data from openweatherAPI
        url = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_name},{country_name}&appid={get_api_key()}&units=metric")
        weather_result = url.json()

        #stores data to variables from API
        city = str(weather_result['name'])
        temp = int(weather_result['main']['temp'])
        temp_min = int(weather_result['main']['temp_min'])
        temp_max = int(weather_result['main']['temp_max'])
        feels_like = int(weather_result['main']['feels_like'])
        discription = str(weather_result['weather'][0]['description'])
        visibility = int(weather_result['visibility'])
        humidity = int(weather_result['main']['humidity'])
        wind_speed = int(weather_result['wind']['speed'])
        #background change depends on this
        background_id = int(weather_result['weather'][0]['id'])

        #change background image url

        #render result page
        return render_template("result.html", city=city, temp=temp, temp_min=temp_min, temp_max=temp_max, feels_like=feels_like, discription=discription, visibility=visibility, humidity=humidity, wind_speed=wind_speed)

    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)