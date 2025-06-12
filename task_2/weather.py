import pandas as pd
import requests


base_url = "https://api.open-meteo.com/v1/forecast"
base_weather_params = {
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ],
    "timezone": "auto",
}
cities = {
    "Калининград": {"latitude": 54.72, "longitude": 20.51},
    "Волгоград": {"latitude": 48.70, "longitude": 44.52},
    "Санкт-Петербург": {"latitude": 59.94, "longitude": 30.31},
    "Москва": {"latitude": 55.75, "longitude": 37.62},
    "Уфа": {"latitude": 54.73, "longitude": 56.00},
    "Екатеринбург": {"latitude": 56.83, "longitude": 60.58},
    "Архангельск": {"latitude": 64.54, "longitude": 40.54},
    "Новосибирск": {"latitude": 55.02, "longitude": 82.93},
    "Якутск": {"latitude": 62.04, "longitude": 129.68},
    "Благовещенск": {"latitude": 50.27, "longitude": 127.54},
}
columns = [
    "Город",
    "Дата и время (ISO 8601)",
    "Температура (°C)",
    "Влажность (%)",
    "Осадки (mm)",
]


def main(cities: dict[str, dict[str, float]]) -> None:
    cities_weather_data = []
    for city, coordinates in cities.items():
        response = requests.get(
            base_url,
            params={
                "latitude": coordinates["latitude"],
                "longitude": coordinates["longitude"],
                "current": base_weather_params["current"],
                "timezone": base_weather_params["timezone"],
            },
        )
        weather_info = response.json()["current"]
        cities_weather_data.append(
            [
                city,
                weather_info["time"],
                weather_info["temperature_2m"],
                weather_info["relative_humidity_2m"],
                weather_info["precipitation"],
            ]
        )
    result = pd.DataFrame(data=cities_weather_data, columns=columns)
    result.to_excel("./result.xlsx", index=False)


if __name__ == "__main__":
    main(cities)
