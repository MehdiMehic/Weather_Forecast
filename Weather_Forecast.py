import requests

def get_coordinates(city_name: str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return result["latitude"], result["longitude"], result["name"], result.get("country", "")
    return None

def get_weather(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        return response.json().get("current_weather", {})
    return None

def get_activity_advice(temp_c: float, is_day: int, weather_code: int):
    advice = []

    if temp_c >= 25:
        advice.append("Its warm outside-stay hydrated!")
    elif temp_c <= 10:
        advice.append("Its cold out there-wear a jacket!")
    else:
        advice.append("Moderate temperature=-perfect weather for a walk.")

    if weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        advice.append("Its raining! Take and umbrella or stay inside")
    elif weather_code >= 71 and weather_code <= 77:
        advice.append("Its snowing!")
    elif weather_code == 0:
        advice.append("Clear sky ahead")

    return "\n".join(f"  - {line}" for line in advice)

def run_weather_advisor():
    city = input("Enter a city name (e.g., Sarajevo, Mostar, ...): ").strip()
    if not city:
        print("City name cannot be empty.")
        return

    print(f"\nFetching weather data for '{city}'...")
    location = get_coordinates(city)

    if not location:
        print("Could not find city coordinates. Check for spelling mistakes.")
        return

    lat, lon, city_official, country = location
    weather = get_weather(lat, lon)

    if not weather:
        print("Failed to retrieve weaather data.")
        return

    temp = weather.get("temperature")
    wind_speed = weather.get("windspeed")
    weather_code = weather.get("weathercode")
    is_day = weather.get("is_day", 1)

    print("\n" + "=" * 40)
    print(f"WEATHER REPORT: {city_official}, {country}")
    print("=" * 40)
    print(f" --- Temperature: {temp} °C")
    print(f" --- Wind speed: {wind_speed} km/h")
    print("\n[ RECOMMENDATIONS ]")
    print(get_activity_advice(temp, is_day, weather_code))
    print("=" * 40 + "\n")

if __name__ == "__main__":
    run_weather_advisor()