import requests

def get_weather_forecast(location, date):
    url = f"https://wttr.in/{location}?date={date}&format=%C+%t+%h+%w"

    response = requests.get(url)

    if response.status_code == 200:
        print("Weather forecast for", date, "in", location)
        print(response.text)
    else:
        print("Failed to retrieve weather data.")

if __name__ == "__main__":
    date = input("Enter date (YYYY-MM-DD): ")
    get_weather_forecast("Dubai,UAE" , date)