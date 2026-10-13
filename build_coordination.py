import os

project_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/agri_dt_backend"
coord_dir = f"{project_dir}/apps/coordination"
os.makedirs(coord_dir, exist_ok=True)

# conflict_detector.py
detector_content = """def detect_conflicts(agent_outputs):
    conflicts = []
    
    growth = agent_outputs.get('crop_growth', {})
    weather = agent_outputs.get('weather', {})
    pest = agent_outputs.get('pest', {})
    
    # Example conflict: irrigation recommended but rain forecasted
    if growth.get('water_need', 0) > 0.5 and weather.get('rain_forecast_7day', 0) > 20:
        conflicts.append({
            'type': 'irrigation_vs_rain',
            'severity': 20,
            'description': 'Irrigation needed but heavy rain forecasted.'
        })
        
    # Example conflict: high humidity and pest risk vs irrigation
    if pest.get('risk_category') == 'high' and weather.get('rain_forecast_7day', 0) > 10:
        conflicts.append({
            'type': 'pest_vs_humidity',
            'severity': 30,
            'description': 'Pest risk is high and rain is forecasted, increasing fungal risk.'
        })

    return conflicts
"""

with open(f"{coord_dir}/conflict_detector.py", "w") as f:
    f.write(detector_content)

# resolver.py (with trace)
resolver_content = """from .conflict_detector import detect_conflicts

def resolve_outputs(agent_outputs):
    conflicts = detect_conflicts(agent_outputs)
    
    trace = []
    
    # Trace step 1: Growth
    growth = agent_outputs.get('crop_growth', {})
    trace.append({
        'step': 1, 'actor': 'CropGrowthAgent', 
        'statement': growth.get('reason', 'No data'), 
        'confidence': growth.get('confidence', 0.5)
    })
    
    # Trace step 2: Weather
    weather = agent_outputs.get('weather', {})
    trace.append({
        'step': 2, 'actor': 'WeatherAgent', 
        'statement': weather.get('reason', 'No data'), 
        'confidence': 0.8
    })
    
    # Trace step 3: Pest
    pest = agent_outputs.get('pest', {})
    trace.append({
        'step': 3, 'actor': 'PestDiseaseAgent', 
        'statement': pest.get('reason', 'No data'), 
        'confidence': 0.7
    })

    if conflicts:
        for c in conflicts:
            trace.append({
                'step': len(trace)+1, 'actor': 'ConflictDetector',
                'statement': c['description'], 'conflict': True
            })
        final_rec = "Hold irrigation, monitor for pests."
    else:
        final_rec = "Proceed with standard growth schedule."
        
    trace.append({
        'step': len(trace)+1, 'actor': 'Resolver',
        'statement': f"Resolution: {final_rec}", 'final': True
    })
    
    yield_data = agent_outputs.get('yield', {})

    return {
        'final_recommendation': final_rec,
        'yield_prediction': yield_data,
        'conflicts_detected': conflicts,
        'explanation': final_rec,
        'reasoning_trace': trace,
        'risk_flags': [c['type'] for c in conflicts],
        'agent_outputs': agent_outputs
    }
"""

with open(f"{coord_dir}/resolver.py", "w") as f:
    f.write(resolver_content)

# trust_score.py
trust_score_content = """def compute_trust_score(agent_outputs, field, coordination_result):
    conflicts = coordination_result.get('conflicts_detected', [])
    
    # Agreement score
    conflict_penalty = sum(c.get('severity', 10) for c in conflicts)
    agreement_score = max(0, 100 - conflict_penalty)
    
    # Data recency score (mocking days_since_last_update as 1 for now)
    days_since_last_update = 1
    recency_score = max(40, 100 - (days_since_last_update * 4.28)) # Decays to 40 in 14 days
    
    # Historical accuracy score
    historical_score = 70 # Default for not enough data
    if field and hasattr(field, 'records') and field.records.count() > 3:
        historical_score = 85 # Mock calculation based on past MAE
        
    trust_score = round(0.4 * agreement_score + 0.3 * recency_score + 0.3 * historical_score)
    
    if trust_score < 50:
        trust_label = "Low"
    elif trust_score < 75:
        trust_label = "Moderate"
    else:
        trust_label = "High"
        
    return {
        'trust_score': trust_score,
        'breakdown': {
            'agreement': round(agreement_score),
            'recency': round(recency_score),
            'historical': round(historical_score)
        },
        'trust_label': trust_label
    }
"""

with open(f"{coord_dir}/trust_score.py", "w") as f:
    f.write(trust_score_content)

print("Coordination files written.")
