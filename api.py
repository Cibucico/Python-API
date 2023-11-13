from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key
OPENWEATHERMAP_API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'
OPENWEATHERMAP_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric',  # You can change to 'imperial' for Fahrenheit
    }

    response = requests.get(OPENWEATHERMAP_API_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()

        # Extract relevant information from the API response
        main_info = weather_data['main']
        weather_info = weather_data['weather'][0]
        temperature = main_info['temp']
        description = weather_info['description']

        result = {
            'city': city,
            'temperature': temperature,
            'description': description,
        }

        return jsonify(result)
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 500

if __name__ == '__main__':
    app.run(debug=True)