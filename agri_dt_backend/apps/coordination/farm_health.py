def compute_farm_health_index(agent_outputs, field_data):
    """
    Computes holistic Farm Health Index (0-100) and component breakdown:
    - 30% Crop Health: Based on vegetative growth stage and biomass expansion rate
    - 25% Water/Soil Health: Root-zone moisture saturation vs crop optimum
    - 25% Pest/Disease Health: Inverted biosecurity score (100 - pest_risk*100)
    - 20% Climate Stability: Thermal & precipitation variance from regional baseline
    """
    growth = agent_outputs.get('crop_growth', {})
    weather = agent_outputs.get('weather', {})
    pest = agent_outputs.get('pest', {})

    # 1. Crop Health (30%)
    growth_conf = growth.get('confidence', 0.8)
    growth_stage = growth.get('growth_stage', 50.0)
    # Healthy crop maintains strong biomass expansion
    crop_health = min(100.0, max(20.0, growth_conf * 100.0))

    # 2. Water / Soil Health (25%)
    soil_moisture = float(field_data.get('soil_moisture', 50.0))
    # Optimal range is 45% - 75%
    if 45.0 <= soil_moisture <= 75.0:
        water_health = 95.0
    elif 30.0 <= soil_moisture < 45.0 or 75.0 < soil_moisture <= 85.0:
        water_health = 75.0
    else:
        water_health = 45.0

    # 3. Pest / Disease Health (25%)
    pest_risk = float(pest.get('pest_risk_score', 0.15))
    pest_health = max(10.0, min(100.0, (1.0 - pest_risk) * 100.0))

    # 4. Climate Stability (20%)
    temp_risk = weather.get('temp_risk_level', 'low')
    extreme = weather.get('extreme_event_risk', False)
    if extreme:
        climate_health = 35.0
    elif temp_risk == 'high':
        climate_health = 55.0
    elif temp_risk == 'medium':
        climate_health = 78.0
    else:
        climate_health = 92.0

    # Composite weighted score
    composite = (0.30 * crop_health) + (0.25 * water_health) + (0.25 * pest_health) + (0.20 * climate_health)
    final_score = int(round(composite))

    if final_score >= 80:
        rating = "OPTIMAL"
    elif final_score >= 60:
        rating = "VIGOROUS"
    elif final_score >= 40:
        rating = "STRESSED"
    else:
        rating = "CRITICAL"

    return {
        "score": final_score,
        "rating": rating,
        "breakdown": {
            "crop_health": int(round(crop_health)),
            "water_soil_health": int(round(water_health)),
            "pest_disease_health": int(round(pest_health)),
            "climate_stability": int(round(climate_health))
        }
    }
