import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

class NASAPowerClient:
    """
    Client for NASA POWER agrometeorology API.
    Provides live daily solar radiation, 2m air temperature, precipitation, and relative humidity.
    Includes in-memory time-based caching and fallback to Tamil Nadu agroclimatic seasonal normals.
    """
    _cache = {}

    DEFAULT_FALLBACK = {
        "temperature": 28.5,
        "rainfall": 12.0,
        "humidity": 68.0,
        "solar_radiation": 18.2,
        "source": "EXTERNAL_FALLBACK"
    }

    def fetch_weather(self, latitude, longitude, date_str=None):
        cache_key = f"{round(latitude, 2)}_{round(longitude, 2)}_{date_str or 'today'}"
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            # 1 hour cache duration
            if (datetime.now() - timestamp).total_seconds() < 3600:
                return cached_data

        target_date = datetime.now() if not date_str else datetime.strptime(date_str, "%Y-%m-%d")
        start_date = (target_date - timedelta(days=2)).strftime("%Y%m%d")
        end_date = target_date.strftime("%Y%m%d")

        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters=T2M,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN&"
            f"community=AG&longitude={longitude}&latitude={latitude}&"
            f"start={start_date}&end={end_date}&format=JSON"
        )

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'AgriDigitalTwin/2.4'})
            with urllib.request.urlopen(req, timeout=4) as response:
                if response.status == 200:
                    payload = json.loads(response.read().decode('utf-8'))
                    params = payload.get('properties', {}).get('parameter', {})
                    t2m_dict = params.get('T2M', {})
                    precip_dict = params.get('PRECTOTCORR', {})
                    rh_dict = params.get('RH2M', {})
                    sw_dict = params.get('ALLSKY_SFC_SW_DWN', {})

                    latest_day = sorted(t2m_dict.keys())[-1] if t2m_dict else None
                    if latest_day and t2m_dict[latest_day] != -999:
                        result = {
                            "temperature": round(float(t2m_dict.get(latest_day, 28.0)), 1),
                            "rainfall": max(0.0, round(float(precip_dict.get(latest_day, 0.0)), 1)),
                            "humidity": round(float(rh_dict.get(latest_day, 65.0)), 1),
                            "solar_radiation": round(float(sw_dict.get(latest_day, 18.0)), 1),
                            "source": "EXTERNAL_NASA_POWER"
                        }
                        self._cache[cache_key] = (result, datetime.now())
                        return result
        except Exception:
            pass

        # Return calibrated Tamil Nadu climatic normal if network unavailable or rate limited
        fallback_res = dict(self.DEFAULT_FALLBACK)
        # Regional adjustment based on latitude
        if latitude > 12.0:
            fallback_res["temperature"] = 29.5
            fallback_res["humidity"] = 62.0
        elif latitude < 10.0:
            fallback_res["temperature"] = 27.8
            fallback_res["humidity"] = 74.0

        return fallback_res
