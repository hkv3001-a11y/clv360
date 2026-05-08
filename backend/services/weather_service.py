import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

WEATHER_LOCATION = os.environ.get("WEATHER_LOCATION", "Nashville, TN")

_cache: dict = {}
CACHE_TTL = 1800  # 30 minutes

WMO_CODES = {
    0: ("Clear sky", "☀️"), 1: ("Mainly clear", "🌤️"), 2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"), 45: ("Fog", "🌫️"), 48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"), 53: ("Moderate drizzle", "🌦️"), 55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"), 63: ("Moderate rain", "🌧️"), 65: ("Heavy rain", "🌧️"),
    71: ("Slight snow", "🌨️"), 73: ("Moderate snow", "🌨️"), 75: ("Heavy snow", "❄️"),
    80: ("Slight showers", "🌦️"), 81: ("Moderate showers", "🌧️"), 82: ("Violent showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm w/ hail", "⛈️"), 99: ("Thunderstorm", "⛈️"),
}


def _wmo(code: int) -> tuple[str, str]:
    return WMO_CODES.get(code, ("Unknown", "🌡️"))


async def get_weather() -> dict:
    now = time.time()
    if "data" in _cache and now - _cache.get("ts", 0) < CACHE_TTL:
        return _cache["data"]

    async with httpx.AsyncClient() as client:
        geo = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": WEATHER_LOCATION, "count": 1, "language": "en", "format": "json"},
            timeout=10.0,
        )
        geo.raise_for_status()
        results = geo.json().get("results", [])
        if not results:
            return {"error": f"Location not found: {WEATHER_LOCATION}"}

        lat, lon = results[0]["latitude"], results[0]["longitude"]

        wx = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m,relative_humidity_2m",
                "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "precipitation_unit": "inch",
                "timezone": "auto",
                "forecast_days": 7,
            },
            timeout=10.0,
        )
        wx.raise_for_status()

    raw = wx.json()
    current = raw["current"]
    daily = raw["daily"]
    desc, emoji = _wmo(current["weather_code"])

    forecast = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(7):
        d, e = _wmo(daily["weather_code"][i])
        forecast.append({
            "date": daily["time"][i],
            "day": days[i % 7],
            "high": round(daily["temperature_2m_max"][i]),
            "low": round(daily["temperature_2m_min"][i]),
            "description": d,
            "emoji": e,
            "precipitation_inches": daily["precipitation_sum"][i],
        })

    data = {
        "location": WEATHER_LOCATION,
        "temp_f": round(current["temperature_2m"]),
        "feels_like_f": round(current["apparent_temperature"]),
        "description": desc,
        "emoji": emoji,
        "wind_mph": round(current["wind_speed_10m"]),
        "humidity": current["relative_humidity_2m"],
        "forecast": forecast,
    }
    _cache.update({"data": data, "ts": now})
    return data
