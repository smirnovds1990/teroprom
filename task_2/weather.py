import pandas as pd
import requests
from requests.exceptions import HTTPError, Timeout


BASE_URL = "https://api.open-meteo.com/v1/forecast"
BASE_WEATHER_PARAMS = {
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ],
    "timezone": "auto",
}
COLUMNS = [
    "Город",
    "Дата и время (ISO 8601)",
    "Температура (°C)",
    "Влажность (%)",
    "Осадки (mm)",
]
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


def make_request_to_weather_api(
    latitude: float, longitude: float
) -> dict[str, str | int | float]:
    response = requests.get(
            BASE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": BASE_WEATHER_PARAMS["current"],
                "timezone": BASE_WEATHER_PARAMS["timezone"],
            },
            timeout=3,
        )
    response.raise_for_status()
    return response.json()["current"]


def get_cities_weather_data(
    cities: dict[str, dict[str, float]]
) -> list[list[str | float | int]]:
    cities_weather_data = []
    for city, coordinates in cities.items():
        weather_info = make_request_to_weather_api(
            coordinates["latitude"], coordinates["longitude"]
        )
        cities_weather_data.append(
            [
                city,
                weather_info["time"],
                weather_info["temperature_2m"],
                weather_info["relative_humidity_2m"],
                weather_info["precipitation"],
            ]
        )
    return cities_weather_data


def write_weather_data_to_excel_file(
    weather_data: list[list[str | float | int]]
) -> None:
    result = pd.DataFrame(data=weather_data, columns=COLUMNS)
    result.to_excel("./result.xlsx", index=False)


def main(cities: dict[str, dict[str, float]]) -> None:
    cities_weather_data = get_cities_weather_data(cities)
    write_weather_data_to_excel_file(cities_weather_data)


if __name__ == "__main__":
    try:
        main(cities)
    except HTTPError as error:
        print(f"Ошибка при запросе. {error}")
    except Timeout as error:
        print(f"Превышено время ожидания ресурса. {error}")
