const apiKey = 'd464355f8cb80fe379285a0d20892923'; // 발급받은 API 키를 여기에 입력
document.getElementById('getWeather').addEventListener('click', () => {
    const city = document.getElementById('city').value;
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.cod === 200) {
                const weatherDiv = document.getElementById('weather');
                weatherDiv.innerHTML = `
                    <h2>${data.name}</h2>
                    <p>Temperature: ${data.main.temp}°C</p>
                    <p>Weather: ${data.weather[0].description}</p>
                    <p>Wind Speed: ${data.wind.speed} m/s</p>
                `;
            } else {
                alert('City not found!');
            }
        })
        .catch(error => console.error('Error:', error));
});
