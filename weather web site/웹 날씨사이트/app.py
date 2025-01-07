from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OpenWeatherMap API 키
api_key = 'd464355f8cb80fe379285a0d20892923'

# 즐겨찾기 리스트
favorites = []

# 번역 함수 대체 (직접 구현)
def _(text):
    return text

@app.route('/', methods=['GET', 'POST'])
def home():
    """홈 페이지"""
    weather_data = None
    if request.method == 'POST':  # 검색 요청
        city_name = request.form.get('city')
        weather_data = fetch_weather(city_name)

    return render_template('index.html', weather=weather_data, favorites=favorites, _=_)

@app.route('/weather/<city_name>')
def favorite_weather(city_name):
    """즐겨찾기 버튼 클릭 시 날씨 정보"""
    weather_data = fetch_weather(city_name)
    return render_template('index.html', weather=weather_data, favorites=favorites, _=_)

@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    """즐겨찾기에 도시 추가"""
    city_name = request.form.get('city')
    if city_name and city_name not in favorites:
        favorites.append(city_name)
    return redirect(url_for('home'))

@app.route('/remove_favorite', methods=['POST'])
def remove_favorite():
    """즐겨찾기에서 도시 제거"""
    city_name = request.form.get('city')
    if city_name in favorites:
        favorites.remove(city_name)
    return redirect(url_for('home'))

def fetch_weather(city_name):
    """날씨 데이터를 OpenWeatherMap에서 가져오는 함수"""
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
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
        return {'error': _('City not found. Please try again.')}

if __name__ == '__main__':
    app.run(debug=True)
