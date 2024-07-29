import requests

def get_weather(city):
    api_key = "4991af48f1baa03672b68e248560b737"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&appid=" + api_key
    response = requests.get(complete_url)
    return response.json()


#python app.py
