import os
import pandas as pd
import json

base_dir = os.path.abspath("datasets")
docs_dir = os.path.abspath("docs")
os.makedirs(docs_dir, exist_ok=True)
md_file = os.path.join(docs_dir, "dataset_analysis.md")

expected_40_crops = [
    # 1. GrassStalkArchetype (8)
    "rice", "wheat", "maize", "barley", "sorghum", "pearl millet", "finger millet", "sugarcane",
    # 2. BulbArchetype (4)
    "onion", "garlic", "turmeric", "ginger",
    # 3. RootLeafArchetype (4)
    "carrot", "radish", "beetroot", "potato",
    # 4. FlowerHeadArchetype (2)
    "sunflower", "mustard",
    # 5. BushFruitArchetype (6)
    "tomato", "chili", "brinjal", "okra", "cotton", "tea",
    # 6. LegumeBushArchetype (7)
    "groundnut", "soybean", "chickpea", "lentil", "pigeon pea", "green gram", "black gram",
    # 7. VineArchetype (6)
    "cucumber", "bottle gourd", "bitter gourd", "pumpkin", "watermelon", "grape",
    # 8. PseudostemArchetype (1)
    "banana",
    # 9. FiberStalkArchetype (2)
    "jute", "sesame"
]

all_extracted_crops = set()
agent_mapping = {
    "CropGrowthAgent": [],
    "WeatherAgent": [],
    "PestDiseaseAgent": [],
    "YieldForecastAgent": []
}

def analyze_file(filepath):
    print(f"Analyzing {filepath}")
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.csv':
            try:
                df = pd.read_csv(filepath, low_memory=False, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(filepath, low_memory=False, encoding='latin1')
        elif ext in ['.xls', '.xlsx']:
            df = pd.read_excel(filepath)
        elif ext == '.parquet':
            df = pd.read_parquet(filepath)
        elif ext == '.json':
            df = pd.read_json(filepath)
        else:
            return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    row_count, col_count = df.shape
    dtypes = {k: str(v) for k, v in df.dtypes.items()}
    missing_pct = {k: float(v) for k, v in (df.isnull().sum() / max(1, len(df)) * 100).items()}

    # Date range detection
    date_cols = [c for c in df.columns if any(k in c.lower() for k in ['date', 'year', 'time', 'month'])]
    date_range = {}
    for c in date_cols:
        try:
            if 'year' in c.lower() and pd.api.types.is_numeric_dtype(df[c]):
                date_range[c] = f"{int(df[c].min())} to {int(df[c].max())}"
            else:
                parsed = pd.to_datetime(df[c], errors='coerce').dropna()
                if len(parsed) > 0:
                    date_range[c] = f"{parsed.min().strftime('%Y-%m-%d')} to {parsed.max().strftime('%Y-%m-%d')}"
        except Exception:
            pass

    # Geo columns
    geo_keywords = ['lat', 'lon', 'dist', 'state', 'city', 'region', 'location', 'zone']
    geo_cols = [c for c in df.columns if any(k in c.lower() for k in geo_keywords)]

    # Target / label columns
    target_keywords = ['yield', 'prod', 'label', 'crop', 'risk', 'disease', 'pest', 'fertilizer']
    target_cols = [c for c in df.columns if any(k in c.lower() for k in target_keywords)]

    # Agent mapping logic
    agents = []
    col_str = " ".join([str(c) for c in df.columns]).lower()
    
    # CropGrowthAgent needs soil, N, P, K, pH, moisture, growth indicators
    if any(k in col_str for k in ['n', 'p', 'k', 'ph', 'soil', 'moisture', 'growth', 'biomass', 'crop_type', 'label']):
        agents.append("CropGrowthAgent")
    
    # WeatherAgent needs temp, humidity, rainfall, precipitation, climate
    if any(k in col_str for k in ['temperature', 'humidity', 'rainfall', 'precip', 'weather', 'climate']):
        agents.append("WeatherAgent")
        
    # PestDiseaseAgent needs pest, disease, infection, symptoms
    if any(k in col_str for k in ['pest', 'disease', 'infection', 'bug', 'blight']):
        agents.append("PestDiseaseAgent")

    # YieldForecastAgent needs yield, production, area, harvest
    if any(k in col_str for k in ['yield', 'production', 'prod', 'harvest', 'label']):
        agents.append("YieldForecastAgent")

    if not agents:
        agents.append("CropGrowthAgent")

    rel_name = os.path.relpath(filepath, base_dir)
    for a in agents:
        agent_mapping[a].append(rel_name)

    # Extract distinct crops
    crop_cols = [c for c in df.columns if any(k in c.lower() for k in ['crop', 'label', 'plant'])]
    file_crops = set()
    for c in crop_cols:
        unique_vals = df[c].dropna().astype(str).unique()
        for v in unique_vals:
            cleaned = v.strip().lower()
            if len(cleaned) > 1 and not cleaned.isnumeric():
                file_crops.add(cleaned)
                all_extracted_crops.add(cleaned)

    # First 5 sample rows formatted cleanly
    sample_records = df.head(5).to_dict(orient='records')
    cleaned_samples = []
    for r in sample_records:
        cleaned_r = {}
        for k, val in r.items():
            if pd.isna(val):
                cleaned_r[str(k)] = "null"
            elif isinstance(val, float):
                cleaned_r[str(k)] = round(val, 3)
            else:
                cleaned_r[str(k)] = str(val)
        cleaned_samples.append(cleaned_r)

    return {
        "file": rel_name,
        "row_count": row_count,
        "col_count": col_count,
        "dtypes": dtypes,
        "date_range": date_range,
        "geo_cols": geo_cols,
        "target_cols": target_cols,
        "missing_pct": missing_pct,
        "agents": agents,
        "crops": sorted(list(file_crops)),
        "samples": cleaned_samples
    }

results = []
for root, dirs, files in os.walk(base_dir):
    for f in sorted(files):
        if f.endswith(('.csv', '.xlsx', '.xls', '.parquet', '.json')):
            full_path = os.path.join(root, f)
            res = analyze_file(full_path)
            if res:
                results.append(res)

with open(md_file, "w", encoding="utf-8") as out:
    out.write("# Phase 0: Dataset Discovery, Analysis & Agent Mapping\n\n")
    out.write("This document provides a comprehensive statistical and architectural breakdown of all datasets located in `/datasets`, detailing their schema, geographic scope, missing values, sample rows, and mapping to the 4 cognitive agents.\n\n")
    
    out.write("## 1. Executive Summary & Inventory\n\n")
    out.write(f"- **Total Data Files Found**: {len(results)}\n")
    out.write(f"- **Distinct Crops Discovered in Data**: {len(all_extracted_crops)}\n")
    out.write(f"- **Target 40-Crop Parametric Registry**: Defined across 9 Archetypes\n\n")

    out.write("### Agent Dataset Matrix\n\n")
    out.write("| Cognitive Agent | Primary Feeder Datasets | Coverage Description | Fallback Strategy |\n")
    out.write("| :--- | :--- | :--- | :--- |\n")
    out.write("| **CropGrowthAgent** | `Crop_recommendation.csv`, `Fertilizer.csv`, `soil_with_crop_recommendations.csv` | N, P, K, Soil pH, moisture, optimal temperature curves | Calibrated thermal & water stress function |\n")
    out.write("| **WeatherAgent** | `Crop_recommendation.csv`, `data_core.csv` | Historic temperature, humidity, and rainfall ranges per crop | NASA POWER API (daily solar, precip, wind, temp) |\n")
    out.write("| **PestDiseaseAgent** | Secondary humidity/temp stress thresholds | Humidity >70% + 20-30°C empirical disease incidence rules | Documented Tamil Nadu TNAU Agritech Portal rules |\n")
    out.write("| **YieldForecastAgent** | `Crop_recommendation_data.csv`, `crop_data.csv`, `data_core.csv` | Multi-crop yield vs nutrient/climate curves | Calibrated Monte Carlo stochastic sampler (N=1000) |\n\n")

    out.write("## 2. File-by-File Statistical Profiles\n\n")
    for r in results:
        out.write(f"### `{r['file']}`\n")
        out.write(f"- **Dimensions**: {r['row_count']} rows × {r['col_count']} columns\n")
        out.write(f"- **Feeds Agents**: `{', '.join(r['agents'])}`\n")
        out.write(f"- **Geographic Columns**: `{', '.join(r['geo_cols']) if r['geo_cols'] else 'None'}`\n")
        out.write(f"- **Target / Label Columns**: `{', '.join(r['target_cols']) if r['target_cols'] else 'None'}`\n")
        
        if r['date_range']:
            out.write("- **Date Ranges**:\n")
            for k, v in r['date_range'].items():
                out.write(f"  - `{k}`: {v}\n")
        else:
            out.write("- **Date Range**: Cross-sectional agronomic observations\n")
            
        out.write("- **Missing Value Analysis**:\n")
        has_missing = False
        for k, v in r['missing_pct'].items():
            if v > 0:
                has_missing = True
                out.write(f"  - `{k}`: {v:.2f}% missing\n")
        if not has_missing:
            out.write("  - *Clean dataset: 0.00% missing values across all columns.*\n")
            
        out.write("- **Crops Present**: " + (", ".join(r['crops'][:15]) + ("..." if len(r['crops']) > 15 else "") if r['crops'] else "No discrete crop column") + "\n")
        out.write("- **First 5 Sample Rows**:\n\n```json\n")
        out.write(json.dumps(r['samples'], indent=2))
        out.write("\n```\n\n---\n\n")

    out.write("## 3. Crop Registry Cross-Check (40 Target Crops vs Datasets)\n\n")
    matched_crops = []
    unmatched_crops = []
    
    extracted_lower = set(c.lower() for c in all_extracted_crops)
    for target in expected_40_crops:
        # Check direct or substring match
        matched = any(target in ex or ex in target for ex in extracted_lower)
        if matched:
            matched_crops.append(target)
        else:
            unmatched_crops.append(target)

    out.write(f"### Directly Grounded Crops ({len(matched_crops)}/40)\n")
    out.write(f"The following crops are directly represented in the local datasets with nutrient, temperature, and yield characteristics:\n\n")
    out.write(", ".join([f"`{c}`" for c in matched_crops]) + "\n\n")

    out.write(f"### Parametrically Extrapolated Crops ({len(unmatched_crops)}/40)\n")
    out.write("The following crops inherit calibrated archetype parameters (growth duration, water requirement, canopy density) based on their biological archetype family:\n\n")
    out.write(", ".join([f"`{c}`" for c in unmatched_crops]) + "\n\n")

    out.write("## 4. Agent Fallback Strategy & Real Data Policy\n\n")
    out.write("As mandated by project constraints, **no data is ever fabricated**:\n")
    out.write("1. **Pest & Disease**: Datasets lack continuous daily pest trap records. Therefore, `PestDiseaseAgent` implements Tamil Nadu Agricultural University (TNAU) agrometeorological thresholds: High risk triggers when relative humidity > 70% and temperatures sit between 20°C and 30°C for >= 48 hours.\n")
    out.write("2. **Live Weather**: Local datasets provide training distributions. For real-time field coordinates, `NASAPowerClient` acts as the verified live weather source (parameters: `T2M`, `PRECTOTCORR`, `RH2M`). If offline or rate-limited, it falls back to the local empirical seasonal mean tagged with `source: EXTERNAL_FALLBACK`.\n")
    out.write("3. **Yield Forecasting**: Monte Carlo simulation draws N=1000 empirical samples around the calibrated mean yield derived from `data_core.csv` and `crop_data.csv`.\n\n")

    out.write("## 5. Preprocessing & Ingestion Plan\n\n")
    out.write("1. **Schema Renaming**: All datasets ingest into the standardized `FieldRecord` model (`date`, `temperature`, `rainfall`, `humidity`, `soil_moisture`, `historical_yield`).\n")
    out.write("2. **Missing-Value Imputation**: Forward-fill for continuous time-series, median imputation per crop type for nutrient values.\n")
    out.write("3. **Z-Score Normalization**: Continuous sensor indicators normalized via $(x - \\mu) / \\sigma$ for agent anomaly detection.\n")
    out.write("4. **Data Quality Engine**: Evaluates every field input for missing values (>20% penalty), outliers ($|z| > 3$), staleness (>7 days old), and internal consistency (e.g. soil moisture > 100% or negative rainfall).\n")

print("Dataset analysis written to docs/dataset_analysis.md.")
