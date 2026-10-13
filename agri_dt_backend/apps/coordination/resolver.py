from .conflict_detector import detect_conflicts
from .farm_health import compute_farm_health_index

def resolve_outputs(agent_outputs, field_data=None):
    """
    Cognitive arbitration layer:
    1. Inspects outputs from CropGrowthAgent, WeatherAgent, PestDiseaseAgent, YieldForecastAgent.
    2. Runs conflict detector to surface contradictions.
    3. Builds step-by-step structured reasoning_trace for EXAI explainability.
    4. Generates single coherent final recommendation.
    5. Computes farm_health_index and provenance_summary.
    """
    conflicts = detect_conflicts(agent_outputs)
    trace = []

    # Step 1: Crop Growth Evaluation
    growth = agent_outputs.get('crop_growth', {})
    trace.append({
        'step': 1,
        'actor': 'CropGrowthAgent',
        'statement': growth.get('reason', 'Crop growth telemetry evaluated.'),
        'confidence': growth.get('confidence', 0.85),
        'conflict': False,
        'final': False
    })

    # Step 2: Weather Evaluation
    weather = agent_outputs.get('weather', {})
    trace.append({
        'step': 2,
        'actor': 'WeatherAgent',
        'statement': weather.get('reason', 'Meteorological forecast evaluated.'),
        'confidence': 0.88,
        'conflict': False,
        'final': False
    })

    # Step 3: Pest and Disease Evaluation
    pest = agent_outputs.get('pest', {})
    trace.append({
        'step': 3,
        'actor': 'PestDiseaseAgent',
        'statement': pest.get('reason', 'Biotic stress conditions evaluated.'),
        'confidence': 0.80,
        'conflict': False,
        'final': False
    })

    # Step 4: Yield Evaluation
    yield_data = agent_outputs.get('yield', {})
    yield_mean = yield_data.get('yield_mean', 4000.0)
    p10 = yield_data.get('yield_p10', yield_mean * 0.9)
    p90 = yield_data.get('yield_p90', yield_mean * 1.1)
    trace.append({
        'step': 4,
        'actor': 'YieldForecastAgent',
        'statement': f"Monte Carlo yield expectation is {yield_mean:,.0f} kg/ha (80% credible interval: {p10:,.0f} to {p90:,.0f} kg/ha).",
        'confidence': yield_data.get('confidence', 0.88),
        'conflict': False,
        'final': False
    })

    # Step 5: Conflict Resolution
    if conflicts:
        for c in conflicts:
            trace.append({
                'step': len(trace) + 1,
                'actor': 'ConflictDetector',
                'statement': f"Arbitrating [{c['agent_a']} vs {c['agent_b']}]: {c['description']} -> {c['resolution']}",
                'conflict': True,
                'final': False
            })

        resolutions = [c['resolution'] for c in conflicts]
        final_rec = " ".join(resolutions)
        explanation = (
            f"Detected {len(conflicts)} agronomic conflict(s). "
            f"Prioritized biosecurity and water conservation: {resolutions[0]}"
        )
    else:
        final_rec = "Proceed with scheduled agronomic management; microclimate and vegetative growth are aligned with baseline targets."
        explanation = "All 4 cognitive agents report harmonic parameters without contradictory field directives."

    # Final step in trace
    trace.append({
        'step': len(trace) + 1,
        'actor': 'CognitiveResolver',
        'statement': f"Final Recommendation: {final_rec}",
        'confidence': 0.90,
        'conflict': False,
        'final': True
    })

    risk_flags = [c['issue'] for c in conflicts]
    if weather.get('extreme_event_risk'):
        risk_flags.append('extreme_weather_risk')

    # Farm health calculation
    f_data = field_data or {
        'temperature': weather.get('temperature_current', 28.0),
        'soil_moisture': 55.0,
        'humidity': weather.get('humidity_current', 65.0)
    }
    farm_health = compute_farm_health_index(agent_outputs, f_data)

    # Provenance summary extraction
    provenance = {
        "real": ["field_record.temperature", "field_record.soil_moisture", "field_record.humidity"],
        "external": ["nasa_power_climatology"],
        "user_provided": ["field.crop_type", "field.latitude", "field.longitude"],
        "predicted": ["crop_growth.growth_stage", "crop_growth.biomass_estimate", "pest.pest_risk_score", "yield.yield_mean"],
        "simulated": ["yield.yield_p10", "yield.yield_p50", "yield.yield_p90", "yield.monte_carlo_distribution"]
    }

    return {
        'final_recommendation': final_rec,
        'yield_prediction': yield_data,
        'conflicts_detected': conflicts,
        'explanation': explanation,
        'reasoning_trace': trace,
        'farm_health_index': farm_health,
        'provenance_summary': provenance,
        'risk_flags': risk_flags,
        'agent_outputs': {
            'crop': agent_outputs.get('crop_growth'),
            'weather': agent_outputs.get('weather'),
            'pest': agent_outputs.get('pest'),
            'yield': agent_outputs.get('yield')
        }
    }
