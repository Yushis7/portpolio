from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(city):
    api_key = "4991af48f1baa03672b68e248560b737"
    weather_url = "http://api.openweathermap.org/data/2.5/weather"
    pollution_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    
    weather_params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    weather_response = requests.get(weather_url, params=weather_params)
    weather_data = weather_response.json()
    
    if weather_response.status_code == 200:
        coord = weather_data['coord']
        pollution_params = {
            'lat': coord['lat'],
            'lon': coord['lon'],
            'appid': api_key
        }
        pollution_response = requests.get(pollution_url, params=pollution_params)
        pollution_data = pollution_response.json()
        
        if pollution_response.status_code == 200:
            weather_data['pollution'] = pollution_data['list'][0]
    
    return weather_data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    return render_template('weather.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
