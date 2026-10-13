import os
import numpy as np

# A basic implementation of the agents
agents_py = """import numpy as np

class CropGrowthAgent:
    def run(self, field_data):
        crop = field_data.get('crop_type', 'unknown').lower()
        temp = field_data.get('temperature', 25)
        moisture = field_data.get('soil_moisture', 50)
        
        # Gaussian temp suitability
        opt_temp = 25
        temp_idx = np.exp(-0.5 * ((temp - opt_temp) / 5) ** 2)
        
        # Water stress
        water_stress = max(0, min(1, moisture / 100))
        
        growth_idx = temp_idx * water_stress
        return {
            "growth_stage": round(growth_idx * 100, 1),
            "biomass_estimate": round(growth_idx * 2000, 2),
            "confidence": round(temp_idx, 2),
            "reason": f"Growth index {growth_idx:.2f} based on temp {temp}C and moisture {moisture}%."
        }

class WeatherAgent:
    def run(self, field_data):
        temp = field_data.get('temperature', 25)
        rain = field_data.get('rainfall', 0)
        
        risk = "low"
        if temp > 35 or temp < 5:
            risk = "high"
        elif temp > 30:
            risk = "medium"
            
        return {
            "rain_forecast_7day": rain * 7,
            "temp_risk_level": risk,
            "reason": f"Risk is {risk} due to temp {temp}C."
        }

class PestDiseaseAgent:
    def run(self, field_data):
        temp = field_data.get('temperature', 25)
        humidity = field_data.get('humidity', 50)
        
        risk = 0.1
        cat = "low"
        
        if humidity > 70 and 20 < temp < 30:
            risk = 0.8
            cat = "high"
        elif humidity > 60:
            risk = 0.5
            cat = "medium"
            
        return {
            "pest_risk_score": risk,
            "risk_category": cat,
            "reason": f"Pest risk is {cat} (Score: {risk}) based on humidity {humidity}%."
        }

class YieldForecastAgent:
    def run(self, field_data):
        crop = field_data.get('crop_type', 'unknown').lower()
        base_yield = 4000
        if 'rice' in crop:
            base_yield = 5000
        elif 'wheat' in crop:
            base_yield = 3500
            
        # Monte Carlo simulation (N=200 for speed as requested in what-if)
        samples = np.random.normal(loc=base_yield, scale=base_yield*0.1, size=200)
        p10 = np.percentile(samples, 10)
        p50 = np.percentile(samples, 50)
        p90 = np.percentile(samples, 90)
        mean_yield = np.mean(samples)
        
        return {
            "yield_mean": float(mean_yield),
            "yield_p10": float(p10),
            "yield_p50": float(p50),
            "yield_p90": float(p90),
            "confidence": 0.85,
            "distribution_samples": [float(x) for x in samples[:10]] # Returning subset for payload
        }
"""
project_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/agri_dt_backend"
os.makedirs(f"{project_dir}/apps/agents", exist_ok=True)
with open(f"{project_dir}/apps/agents/agents.py", "w") as f:
    f.write(agents_py)

print("Agents written.")
