from flask import Flask, render_template, request, redirect, url_for
import requests
from googletrans import Translator
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "your_secret_key"
csrf = CSRFProtect(app)

# OpenWeatherMap API 키
api_key = 'd464355f8cb80fe379285a0d20892923'

# Google Translate Translator 객체 생성
translator = Translator()

# 즐겨찾기 리스트
favorites = []

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city_name = request.form.get('city')
        weather_data = fetch_weather(city_name)
    return render_template('index.html', weather=weather_data, favorites=favorites)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    city_name = request.form.get('city')
    if city_name and city_name not in favorites:
        favorites.append(city_name)
    return redirect(url_for('home'))

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    city_name = request.form.get('city')
    if city_name in favorites:
        favorites.remove(city_name)
    return redirect(url_for('home'))

@app.route('/weather/<city_name>')
def favorite_weather(city_name):
    weather_data = fetch_weather(city_name)
    return render_template('index.html', weather=weather_data, favorites=favorites)

def fetch_weather(city_name):
    try:
        translated_city_name = translator.translate(city_name, src='ko', dest='en').text
    except Exception as e:
        return {'error': 'Translation failed. Please try again.'}

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={translated_city_name}&appid={api_key}&units=metric'
    weather_response = requests.get(weather_url)
    weather = weather_response.json()

    if weather.get('cod') == 200:
        lat = weather['coord']['lat']
        lon = weather['coord']['lon']
        air_pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
        air_response = requests.get(air_pollution_url)
        air_data = air_response.json()

        pm2_5 = air_data['list'][0]['components']['pm2_5']
        pm10 = air_data['list'][0]['components']['pm10']

        return {
            'city': city_name,
            'translated_city': translated_city_name,
            'temperature': weather['main']['temp'],
            'feels_like': weather['main']['feels_like'],
            'humidity': weather['main']['humidity'],
            'pressure': weather['main']['pressure'],
            'description': weather['weather'][0]['description'],
            'lat': lat,
            'lon': lon,
            'pm2_5': pm2_5,
            'pm10': pm10,
        }
    else:
        return {'error': 'City not found. Please try again.'}

if __name__ == '__main__':
    app.run(debug=True)
