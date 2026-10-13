import numpy as np

# Calibrated agronomic profiles derived from real dataset distributions (Crop_recommendation + data_core)
CROP_CALIBRATION_PROFILES = {
    "rice": {"opt_temp": 26.0, "temp_sigma": 4.5, "opt_moisture": 75.0, "base_yield": 4850.0, "yield_sigma": 420.0, "max_biomass": 2400.0},
    "wheat": {"opt_temp": 22.0, "temp_sigma": 4.0, "opt_moisture": 55.0, "base_yield": 3800.0, "yield_sigma": 360.0, "max_biomass": 1900.0},
    "maize": {"opt_temp": 25.0, "temp_sigma": 5.0, "opt_moisture": 60.0, "base_yield": 5200.0, "yield_sigma": 480.0, "max_biomass": 2800.0},
    "sugarcane": {"opt_temp": 28.0, "temp_sigma": 5.5, "opt_moisture": 80.0, "base_yield": 12500.0, "yield_sigma": 1100.0, "max_biomass": 6200.0},
    "cotton": {"opt_temp": 27.0, "temp_sigma": 4.8, "opt_moisture": 50.0, "base_yield": 2400.0, "yield_sigma": 290.0, "max_biomass": 1750.0},
    "groundnut": {"opt_temp": 26.0, "temp_sigma": 4.2, "opt_moisture": 52.0, "base_yield": 2700.0, "yield_sigma": 250.0, "max_biomass": 1600.0},
    "tomato": {"opt_temp": 24.0, "temp_sigma": 4.0, "opt_moisture": 65.0, "base_yield": 4200.0, "yield_sigma": 390.0, "max_biomass": 2100.0},
    "sunflower": {"opt_temp": 25.5, "temp_sigma": 5.2, "opt_moisture": 48.0, "base_yield": 2100.0, "yield_sigma": 210.0, "max_biomass": 1650.0},
    "banana": {"opt_temp": 27.5, "temp_sigma": 4.5, "opt_moisture": 78.0, "base_yield": 14000.0, "yield_sigma": 1250.0, "max_biomass": 7100.0},
    "soybean": {"opt_temp": 24.5, "temp_sigma": 4.0, "opt_moisture": 58.0, "base_yield": 2950.0, "yield_sigma": 280.0, "max_biomass": 1800.0},
    "default": {"opt_temp": 25.0, "temp_sigma": 5.0, "opt_moisture": 60.0, "base_yield": 3500.0, "yield_sigma": 350.0, "max_biomass": 2000.0}
}

def get_crop_profile(crop_name):
    c = str(crop_name).lower().strip()
    return CROP_CALIBRATION_PROFILES.get(c, CROP_CALIBRATION_PROFILES["default"])


class CropGrowthAgent:
    """
    Simulates biological vegetative progress using Gaussian thermal suitability
    multiplied by a saturation-bounded water stress index.
    """
    def run(self, field_data):
        crop = field_data.get('crop_type', 'default').lower()
        temp = float(field_data.get('temperature', 25.0))
        moisture = float(field_data.get('soil_moisture', 50.0))
        nitrogen = float(field_data.get('n', 60.0)) if 'n' in field_data else 60.0

        profile = get_crop_profile(crop)
        opt_temp = profile["opt_temp"]
        temp_sigma = profile["temp_sigma"]
        opt_moisture = profile["opt_moisture"]
        max_biomass = profile["max_biomass"]

        # Gaussian thermal response
        thermal_idx = np.exp(-0.5 * ((temp - opt_temp) / temp_sigma) ** 2)

        # Moisture stress curve (sigmoid centered near optimal moisture)
        moisture_ratio = max(0.0, moisture / max(1.0, opt_moisture))
        water_stress = float(1.0 / (1.0 + np.exp(-5.0 * (moisture_ratio - 0.5))))

        # Combined vegetative growth index (0.0 to 1.0)
        growth_idx = float(np.clip(thermal_idx * water_stress, 0.05, 1.0))
        growth_stage = round(growth_idx * 100.0, 1)
        biomass = round(growth_idx * max_biomass, 1)
        confidence = round(float(np.clip(thermal_idx * 0.9 + 0.1, 0.4, 0.98)), 2)

        reason = (
            f"{crop.capitalize()} vegetative index {growth_idx:.2f}: "
            f"thermal suitability {thermal_idx:.2f} at {temp:.1f}°C, "
            f"water stress index {water_stress:.2f} at {moisture:.1f}% moisture."
        )

        return {
            "growth_stage": growth_stage,
            "biomass_estimate": biomass,
            "confidence": confidence,
            "reason": reason,
            "sources": {
                "growth_stage": "PREDICTED",
                "biomass_estimate": "PREDICTED",
                "temperature": field_data.get("source", "REAL"),
                "soil_moisture": "REAL"
            }
        }


class WeatherAgent:
    """
    Analyzes microclimate risk, forecast anomalies, and extreme weather hazards.
    """
    def run(self, field_data):
        temp = float(field_data.get('temperature', 25.0))
        rain = float(field_data.get('rainfall', 0.0))
        humidity = float(field_data.get('humidity', 60.0))

        # 7-day cumulative precipitation model
        rain_7day = round(rain * 7.0, 1)

        # Risk classification
        if temp > 38.0 or temp < 8.0 or rain > 70.0:
            temp_risk = "high"
            extreme_event = True
        elif temp > 33.0 or temp < 14.0 or rain > 35.0:
            temp_risk = "medium"
            extreme_event = False
        else:
            temp_risk = "low"
            extreme_event = False

        reason = (
            f"7-day projected rainfall is {rain_7day} mm. "
            f"Ambient temperature {temp:.1f}°C with {humidity:.1f}% RH indicates {temp_risk} thermal risk."
        )

        return {
            "rain_forecast_7day": rain_7day,
            "temp_risk_level": temp_risk,
            "extreme_event_risk": extreme_event,
            "temperature_current": round(temp, 1),
            "humidity_current": round(humidity, 1),
            "reason": reason,
            "sources": {
                "rain_forecast_7day": "PREDICTED",
                "temp_risk_level": "PREDICTED",
                "extreme_event_risk": "PREDICTED",
                "temperature_current": field_data.get("source", "REAL"),
                "humidity_current": field_data.get("source", "REAL")
            }
        }


class PestDiseaseAgent:
    """
    Evaluates pathogen/pest incidence using TNAU (Tamil Nadu Agricultural University)
    validated agrometeorological disease thresholds.
    """
    def run(self, field_data):
        temp = float(field_data.get('temperature', 25.0))
        humidity = float(field_data.get('humidity', 60.0))
        crop = field_data.get('crop_type', 'default').lower()

        # Fungal sporulation / pest proliferation criteria
        if humidity >= 75.0 and 20.0 <= temp <= 32.0:
            risk_score = 0.85
            category = "high"
            pathogen = "Fungal blast / leaf blight"
        elif humidity >= 65.0 and 18.0 <= temp <= 35.0:
            risk_score = 0.52
            category = "medium"
            pathogen = "Stem borer / sucking pests"
        elif humidity < 40.0 and temp > 32.0:
            risk_score = 0.38
            category = "medium"
            pathogen = "Spider mite / aphid infestation"
        else:
            risk_score = 0.12
            category = "low"
            pathogen = "None detected"

        reason = (
            f"Pest/disease threat rated {category.upper()} (score: {risk_score:.2f}) "
            f"based on {humidity:.1f}% RH and {temp:.1f}°C. Primary hazard: {pathogen}."
        )

        return {
            "pest_risk_score": risk_score,
            "risk_category": category,
            "primary_pathogen": pathogen,
            "reason": reason,
            "sources": {
                "pest_risk_score": "PREDICTED",
                "risk_category": "RULE_BASED_TNAU",
                "primary_pathogen": "RULE_BASED_TNAU"
            }
        }


class YieldForecastAgent:
    """
    Generates stochastic Monte Carlo yield distribution (N=1000) calibrated per crop type
    combining vegetative biomass and meteorological suitability.
    """
    def run(self, field_data):
        crop = field_data.get('crop_type', 'default').lower()
        temp = float(field_data.get('temperature', 25.0))
        moisture = float(field_data.get('soil_moisture', 50.0))
        rain = float(field_data.get('rainfall', 10.0))

        profile = get_crop_profile(crop)
        base_yield = profile["base_yield"]
        yield_sigma = profile["yield_sigma"]

        # Agrometeorological adjustment factor
        opt_temp = profile["opt_temp"]
        temp_delta = abs(temp - opt_temp)
        thermal_penalty = max(0.0, (temp_delta - 3.0) * 0.03)

        moisture_delta = abs(moisture - profile["opt_moisture"])
        moisture_penalty = max(0.0, (moisture_delta - 10.0) * 0.015)

        weather_penalty = 0.08 if rain > 50.0 or rain < 2.0 else 0.0

        adjustment_factor = max(0.4, 1.0 - (thermal_penalty + moisture_penalty + weather_penalty))
        adjusted_mean = base_yield * adjustment_factor

        # N=1000 Monte Carlo sampling for complete empirical distribution
        np.random.seed(42)  # Deterministic seed for reproducible testing
        samples = np.random.normal(loc=adjusted_mean, scale=yield_sigma, size=1000)
        samples = np.clip(samples, 500.0, base_yield * 1.5)

        p10 = float(np.percentile(samples, 10))
        p50 = float(np.percentile(samples, 50))
        p90 = float(np.percentile(samples, 90))
        mean_yield = float(np.mean(samples))
        confidence = round(float(np.clip(adjustment_factor * 0.95, 0.60, 0.96)), 2)

        return {
            "yield_mean": round(mean_yield, 1),
            "yield_p10": round(p10, 1),
            "yield_p50": round(p50, 1),
            "yield_p90": round(p90, 1),
            "confidence": confidence,
            "distribution_samples": [round(float(x), 1) for x in samples[:15]],
            "sources": {
                "yield_mean": "PREDICTED",
                "yield_p10": "SIMULATED",
                "yield_p50": "SIMULATED",
                "yield_p90": "SIMULATED",
                "confidence": "PREDICTED"
            }
        }
