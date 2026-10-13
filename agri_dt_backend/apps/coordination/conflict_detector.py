def detect_conflicts(agent_outputs):
    """
    Explicit multi-agent rule checks for mutually contradictory recommendations:
    1. Rain forecast vs irrigation need
    2. High humidity / fungal pest risk vs irrigation increase
    3. Severe thermal stress vs harvest delay
    """
    conflicts = []
    
    growth = agent_outputs.get('crop_growth', {})
    weather = agent_outputs.get('weather', {})
    pest = agent_outputs.get('pest', {})
    yield_data = agent_outputs.get('yield', {})

    growth_stage = growth.get('growth_stage', 50.0)
    rain_7day = weather.get('rain_forecast_7day', 0.0)
    pest_risk = pest.get('pest_risk_score', 0.0)
    temp_risk = weather.get('temp_risk_level', 'low')

    # Conflict 1: Growth agent indicates water requirement, but weather forecasts precipitation
    if growth_stage < 85.0 and rain_7day >= 20.0:
        conflicts.append({
            'agent_a': 'CropGrowthAgent',
            'agent_b': 'WeatherAgent',
            'issue': 'irrigation_vs_rain',
            'severity': 35,
            'description': f"Crop is in active growth ({growth_stage}%), but heavy precipitation ({rain_7day:.1f} mm) is forecasted in 7 days.",
            'resolution': 'Withhold supplemental irrigation; allow natural rainfall to replenish the root zone.'
        })

    # Conflict 2: High humidity / fungal pathogen risk exacerbated by high moisture/rain
    if pest_risk >= 0.60 and rain_7day >= 15.0:
        conflicts.append({
            'agent_a': 'PestDiseaseAgent',
            'agent_b': 'WeatherAgent',
            'issue': 'pest_vs_humidity',
            'severity': 45,
            'description': f"High pest/disease vulnerability ({pest.get('primary_pathogen', 'Fungal threat')}) combines with impending rainfall ({rain_7day:.1f} mm) to accelerate spore germination.",
            'resolution': 'Apply preventive bio-fungicide before rain onset; ensure field drainage trenches are clear.'
        })

    # Conflict 3: Extreme thermal risk during maturity stage
    if temp_risk == 'high' and growth_stage > 80.0:
        conflicts.append({
            'agent_a': 'WeatherAgent',
            'agent_b': 'YieldForecastAgent',
            'issue': 'heat_stress_vs_harvest',
            'severity': 30,
            'description': 'Elevated thermal stress during the grain-filling/ripening stage risks grain shattering and yield degradation.',
            'resolution': 'Advance harvest schedule by 3-5 days to preserve test weight and grain quality.'
        })

    return conflicts
