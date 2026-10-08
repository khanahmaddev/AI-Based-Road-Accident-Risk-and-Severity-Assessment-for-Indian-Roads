import urllib.request
import urllib.parse
import json
from typing import Dict, Any

WMO_WEATHER_CODES = {
    0: ("clear", "high"),
    1: ("clear", "high"),
    2: ("cloudy", "high"),
    3: ("cloudy", "medium"),
    45: ("fog", "low"),
    48: ("fog", "low"),
    51: ("rain", "medium"),
    53: ("rain", "medium"),
    55: ("rain", "low"),
    61: ("rain", "medium"),
    63: ("rain", "low"),
    65: ("rain", "low"),
    80: ("rain", "medium"),
    81: ("rain", "low"),
    82: ("rain", "low"),
    95: ("thunderstorm", "low"),
    96: ("thunderstorm", "low"),
    99: ("thunderstorm", "low"),
}

class WeatherClient:
    _cache = {}

    @classmethod
    def get_live_weather(cls, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch real-time weather from Open-Meteo API.
        Cached by rounded coordinate (~10km resolution) to respect API quotas and maintain fast response times.
        """
        cache_key = (round(lat, 1), round(lon, 1))
        if cache_key in cls._cache:
            return cls._cache[cache_key]

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat:.4f}&longitude={lon:.4f}&"
            f"current=temperature_2m,relative_humidity_2m,precipitation,rain,weather_code,wind_speed_10m"
        )
        
        req = urllib.request.Request(url, headers={'User-Agent': 'IndianAccidentRiskApp/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                current = data.get("current", {})
                wcode = current.get("weather_code", 0)
                temp = float(current.get("temperature_2m", 28.0))
                rain_val = float(current.get("rain", 0.0))
                precip = float(current.get("precipitation", 0.0))
                wind = float(current.get("wind_speed_10m", 10.0))
                humidity = float(current.get("relative_humidity_2m", 50.0))

                condition, visibility_cat = WMO_WEATHER_CODES.get(wcode, ("clear", "high"))
                if precip > 0.5 or rain_val > 0.5:
                    condition = "rain"

                result = {
                    "source": "Open-Meteo Realtime API",
                    "condition": condition,
                    "visibility_category": visibility_cat,
                    "temperature_c": temp,
                    "precipitation_mm": precip,
                    "rain_mm": rain_val,
                    "wind_speed_kmh": wind,
                    "humidity_percent": humidity,
                    "weather_code": wcode,
                    "live": True
                }
                cls._cache[cache_key] = result
                return result
        except Exception as e:
            # Fallback to realistic seasonal Indian baseline if offline/timeout
            fallback = {
                "source": "Fallback baseline (API unreachable)",
                "condition": "clear",
                "visibility_category": "high",
                "temperature_c": 28.0,
                "precipitation_mm": 0.0,
                "wind_speed_kmh": 12.0,
                "humidity_percent": 55.0,
                "weather_code": 0,
                "live": False,
                "error": str(e)
            }
            return fallback
