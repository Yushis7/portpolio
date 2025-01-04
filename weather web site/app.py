from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# OpenWeatherMap API 키
api_key = 'd464355f8cb80fe379285a0d20892923'

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None  # 날씨 데이터 초기값
    if request.method == 'POST':  # 사용자가 검색을 시도한 경우
        city_name = request.form.get('city')  # HTML 폼에서 도시 이름 가져오기
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
        weather_response = requests.get(weather_url)
        weather = weather_response.json()

        if weather.get('cod') == 200:  # 날씨 데이터를 성공적으로 가져온 경우
            # 위도와 경도 가져오기
            lat = weather['coord']['lat']
            lon = weather['coord']['lon']

            # 미세먼지 데이터를 가져오기 위한 Air Pollution API 호출
            air_pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
            air_response = requests.get(air_pollution_url)
            air_data = air_response.json()

            # 미세먼지 데이터 가져오기
            pm2_5 = air_data['list'][0]['components']['pm2_5']
            pm10 = air_data['list'][0]['components']['pm10']

            # 데이터를 weather_data에 추가
            weather_data = {
                'city': city_name,
                'temperature': weather['main']['temp'],
                'feels_like': weather['main']['feels_like'],
                'humidity': weather['main']['humidity'],
                'pressure': weather['main']['pressure'],
                'description': weather['weather'][0]['description'],
                'lat': lat,
                'lon': lon,
                'pm2_5': pm2_5,  # PM2.5 농도
                'pm10': pm10,    # PM10 농도
            }
        else:  # 에러 메시지 처리
            weather_data = {'error': 'City not found. Please try again.'}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
