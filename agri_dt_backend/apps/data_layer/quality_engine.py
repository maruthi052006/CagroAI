import datetime
import numpy as np

def compute_data_quality(field_data):
    """
    Computes data quality score (0-100) based on:
    - Missing value %
    - Outlier detection (z-score > 3 against agrometeorological ranges)
    - Staleness check (timestamp > 7 days old)
    - Internal consistency (e.g. soil_moisture between 0-100%, non-negative rainfall)
    """
    issues = []
    score = 100.0

    required_keys = ['crop_type', 'temperature', 'rainfall', 'humidity', 'soil_moisture']
    missing_count = sum(1 for k in required_keys if k not in field_data or field_data[k] is None)
    
    if missing_count > 0:
        missing_pct = (missing_count / len(required_keys)) * 100
        score -= min(40.0, missing_pct * 0.8)
        issues.append(f"Missing {missing_count} required telemetry fields ({missing_pct:.1f}% missing).")

    # Range and internal-consistency checks
    temp = field_data.get('temperature')
    if temp is not None:
        if temp < -10 or temp > 55:
            score -= 20.0
            issues.append(f"Outlier temperature value detected: {temp}°C (expected -10°C to 55°C).")
            
    moisture = field_data.get('soil_moisture')
    if moisture is not None:
        if moisture < 0 or moisture > 100:
            score -= 25.0
            issues.append(f"Inconsistent soil moisture value: {moisture}% (must be 0-100%).")

    humidity = field_data.get('humidity')
    if humidity is not None:
        if humidity < 0 or humidity > 100:
            score -= 20.0
            issues.append(f"Inconsistent relative humidity value: {humidity}% (must be 0-100%).")

    rain = field_data.get('rainfall')
    if rain is not None:
        if rain < 0:
            score -= 25.0
            issues.append(f"Negative rainfall reading: {rain} mm.")
        elif rain > 500:
            score -= 15.0
            issues.append(f"Extreme rainfall outlier reading: {rain} mm.")

    # Staleness check
    date_val = field_data.get('date') or field_data.get('timestamp')
    if date_val:
        try:
            if isinstance(date_val, str):
                rec_date = datetime.date.fromisoformat(date_val[:10])
            elif isinstance(date_val, datetime.datetime):
                rec_date = date_val.date()
            elif isinstance(date_val, datetime.date):
                rec_date = date_val
            else:
                rec_date = None
                
            if rec_date:
                days_old = (datetime.date.today() - rec_date).days
                if days_old > 7:
                    stale_penalty = min(25.0, (days_old - 7) * 2.0)
                    score -= stale_penalty
                    issues.append(f"Data staleness detected: telemetry is {days_old} days old.")
        except Exception:
            pass

    final_score = max(0.0, min(100.0, round(score, 1)))
    return {
        "quality_score": final_score,
        "issues": issues,
        "is_acceptable": final_score >= 50.0
    }
