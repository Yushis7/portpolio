from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_babel import Babel, _
import requests

app = Flask(__name__)

# Babel 설정
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ko']
babel = Babel(app)

# OpenWeatherMap API 키
api_key = 'd464355f8cb80fe379285a0d20892923'

# Babel의 locale 선택 함수
def select_locale():
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

# 즐겨찾기 리스트
favorites = []

@babel.localeselector
def get_locale():
    """사용자의 언어 설정을 결정"""
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

@app.route('/', methods=['GET', 'POST'])
def home():
    """홈 페이지 - 날씨 검색 및 즐겨찾기 관리"""
    weather_data = None
    if request.method == 'POST':  # 검색 요청
        city_name = request.form.get('city')  # 검색창에서 입력된 도시명
        lang = get_locale()  # 언어 설정
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang={lang}'
        weather_response = requests.get(weather_url)
        weather = weather_response.json()

        if weather.get('cod') == 200:  # 데이터 정상 반환
            lat = weather['coord']['lat']
            lon = weather['coord']['lon']
            air_pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
            air_response = requests.get(air_pollution_url)
            air_data = air_response.json()

            pm2_5 = air_data['list'][0]['components']['pm2_5']
            pm10 = air_data['list'][0]['components']['pm10']

            weather_data = {
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
            weather_data = {'error': _('도시를 찾을 수 없습니다. 다시 시도해 주세요.')}

    return render_template('index.html', weather=weather_data, favorites=favorites)

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

if __name__ == '__main__':
    app.run(debug=True)
