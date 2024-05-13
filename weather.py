from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    weather = None
    return render_template('weather.html', weather=weather)


@app.route('/weather', methods=['POST'])
def get_weather():
    pic_icons=[
        "/static/images/sunny.jpeg",
        "/static/images/rain.jpeg",
        "/static/images/cloud.jpeg",
        "/static/images/snowy.jpeg",
        "/static/images/fog.jpeg",
        "/static/images/cloud-sun.jpeg",
        "/static/images/thunder.jpeg",
    ]



    icons=["/static/icons/animated/not_available.jpeg", "/static/icons/animated/not_available.jpeg", "/static/icons/animated/day.svg", "/static/icons/animated/cloudy-day-1.svg", "/static/icons/animated/cloudy-day-2.svg", "/static/icons/animated/cloudy-day-3.svg", "/static/icons/animated/cloudy.svg", "/static/icons/animated/cloudy.svg", "/static/icons/animated/cloudy-day-3.svg", "/static/icons/animated/fog.jpeg", "/static/icons/animated/rainy-4.svg", "/static/icons/animated/rainy-5.svg", "/static/icons/animated/rainy-1.svg", "/static/icons/animated/rainy-6.svg", "/static/icons/animated/thunder.svg", "/static/icons/animated/thunder.svg", "/static/icons/animated/snowy-2.svg", "/static/icons/animated/snowy-4.svg", "/static/icons/animated/snowy-1.svg", "/static/icons/animated/snowy-6.svg", "/static/icons/animated/rainy-7.svg", "/static/icons/animated/rainy-7.svg", "/static/icons/animated/rainy-7.svg", "/static/icons/animated/weather.svg", "/static/icons/animated/weather.svg", "/static/icons/animated/rainy-7.svg", "/static/icons/animated/day.svg", "/static/icons/animated/cloudy-day-1.svg", "/static/icons/animated/cloudy-day-2.svg", "/static/icons/animated/cloudy-day-3.svg", "/static/icons/animated/cloudy.svg", "/static/icons/animated/rainy-1.svg", "/static/icons/animated/rainy-6.svg", "/static/icons/animated/thunder.svg", "/static/icons/animated/snowy-6.svg", "/static/icons/animated/weather.svg", "/static/icons/animated/weather.svg"]

    place = request.form['place']
    url = "https://ai-weather-by-meteosource.p.rapidapi.com/find_places"
    querystring = {"text": place, "language": "en"}
    headers = {
        "X-RapidAPI-Key": "9b162e2384mshcc729ddc7e09ae2p1b0702jsnf43f93d397a7",
        "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        place = response.json()[0]
        latitude = place['lat'][:-1:]
        longitude = place['lon'][:-1:]
    else:
        return render_template('error.html', error='No data found for India')

    url = "https://ai-weather-by-meteosource.p.rapidapi.com/current"
    querystring = {
            "lat": latitude,
            "lon": longitude,
            "timezone": "auto",
            "language": "en",
            "units": "auto"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        weather_data = response.json()
        sunny=[2,3,26,27]
        rain=[10,11,12,13,25,32,23,24,36]
        cloudy=[6,7,8,30,31]
        snowy=[16.17,18,19,20,21,22,35,34]

        fog=[9,1,0]

        thunder=[14,15,33]

        cloudy_sunny=[28,4,5,29]

        if weather_data["current"]["icon_num"] in sunny:
            pic_url=pic_icons[0]
        elif weather_data["current"]["icon_num"] in rain:
            pic_url=pic_icons[1]
        elif  weather_data["current"]["icon_num"] in cloudy:
            pic_url=pic_icons[2]
        elif weather_data["current"]["icon_num"] in snowy:
            pic_url=pic_icons[3]
        elif  weather_data["current"]["icon_num"] in fog:
            pic_url=pic_icons[4]
        elif  weather_data["current"]["icon_num"] in cloudy_sunny:
            pic_url=pic_icons[5]
        elif weather_data["current"]["icon_num"] in thunder:
            pic_url=pic_icons[6]

        #starting of GEt_DAILY request
        url = "https://ai-weather-by-meteosource.p.rapidapi.com/daily"

        querystring = {"lat":latitude,"lon":longitude,"language":"en","units":"auto"}

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            prediction_data=response.json()
            
            return render_template('weather.html', weather=weather_data, prediction=prediction_data, icon=icons, pic_urls=pic_url)
        else:
            return render_template('error.html', error='Failed to fetch weather data'), response.status_code
        #ending of GEt_DAILY request
    else:
        return render_template('error.html', error='Failed to fetch weather data'), response.status_code
if __name__ == '__main__':
    app.run(debug=True)
