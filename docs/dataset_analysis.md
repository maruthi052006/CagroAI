# Phase 0: Dataset Discovery, Analysis & Agent Mapping

This document provides a comprehensive statistical and architectural breakdown of all datasets located in `/datasets`, detailing their schema, geographic scope, missing values, sample rows, and mapping to the 4 cognitive agents.

## 1. Executive Summary & Inventory

- **Total Data Files Found**: 22
- **Distinct Crops Discovered in Data**: 235
- **Target 40-Crop Parametric Registry**: Defined across 9 Archetypes

### Agent Dataset Matrix

| Cognitive Agent | Primary Feeder Datasets | Coverage Description | Fallback Strategy |
| :--- | :--- | :--- | :--- |
| **CropGrowthAgent** | `Crop_recommendation.csv`, `Fertilizer.csv`, `soil_with_crop_recommendations.csv` | N, P, K, Soil pH, moisture, optimal temperature curves | Calibrated thermal & water stress function |
| **WeatherAgent** | `Crop_recommendation.csv`, `data_core.csv` | Historic temperature, humidity, and rainfall ranges per crop | NASA POWER API (daily solar, precip, wind, temp) |
| **PestDiseaseAgent** | Secondary humidity/temp stress thresholds | Humidity >70% + 20-30°C empirical disease incidence rules | Documented Tamil Nadu TNAU Agritech Portal rules |
| **YieldForecastAgent** | `Crop_recommendation_data.csv`, `crop_data.csv`, `data_core.csv` | Multi-crop yield vs nutrient/climate curves | Calibrated Monte Carlo stochastic sampler (N=1000) |

## 2. File-by-File Statistical Profiles

### `archive (1)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (10)\data.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (11)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (12)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (13)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (14)\Crop_recommendation_data.csv`
- **Dimensions**: 7950 rows × 9 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, artichoke, asparagus, banana, barley, beetroot, blackgram, blueberry, broccoli, brussels_sprouts, buckwheat, cabbage, canola, carrot, cauliflower...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice",
    "soil_type": "Clay Loam"
  }
]
```

---

### `archive (14)\Crop_recommendation_data.xlsx`
- **Dimensions**: 7950 rows × 9 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, artichoke, asparagus, banana, barley, beetroot, blackgram, blueberry, broccoli, brussels_sprouts, buckwheat, cabbage, canola, carrot, cauliflower...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice",
    "soil_type": "Clay Loam"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice",
    "soil_type": "Clay Loam"
  }
]
```

---

### `archive (15)\crop_data.csv`
- **Dimensions**: 694 rows × 7 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `CROP`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: aloe vera, amaranth (rajgira), ashwagandha, asparagus, avocado, bamboo, banana, barley, barnyard millet, bittergourd, blackgram, blackpepper, blueberry, bottlegourd, brinjal...
- **First 5 Sample Rows**:

```json
[
  {
    "CROP": "DRAGON FRUIT",
    "N": "100",
    "P": "55",
    "K": "165",
    "PH": 5.7,
    "RAINFALL": 1050.0,
    "TEMP": 32.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "100",
    "P": "60",
    "K": "160",
    "PH": 6.5,
    "RAINFALL": 900.0,
    "TEMP": 32.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "90",
    "P": "30",
    "K": "160",
    "PH": 6.4,
    "RAINFALL": 900.0,
    "TEMP": 31.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "80",
    "P": "40",
    "K": "150",
    "PH": 6.0,
    "RAINFALL": 800.0,
    "TEMP": 30.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "80",
    "P": "45",
    "K": "150",
    "PH": 6.0,
    "RAINFALL": 800.0,
    "TEMP": 34.0
  }
]
```

---

### `archive (16)\Crop_Recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `Crop`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "Nitrogen": "90",
    "Phosphorus": "42",
    "Potassium": "43",
    "Temperature": 20.88,
    "Humidity": 82.003,
    "pH_Value": 6.503,
    "Rainfall": 202.936,
    "Crop": "Rice"
  },
  {
    "Nitrogen": "85",
    "Phosphorus": "58",
    "Potassium": "41",
    "Temperature": 21.77,
    "Humidity": 80.32,
    "pH_Value": 7.038,
    "Rainfall": 226.656,
    "Crop": "Rice"
  },
  {
    "Nitrogen": "60",
    "Phosphorus": "55",
    "Potassium": "44",
    "Temperature": 23.004,
    "Humidity": 82.321,
    "pH_Value": 7.84,
    "Rainfall": 263.964,
    "Crop": "Rice"
  },
  {
    "Nitrogen": "74",
    "Phosphorus": "35",
    "Potassium": "40",
    "Temperature": 26.491,
    "Humidity": 80.158,
    "pH_Value": 6.98,
    "Rainfall": 242.864,
    "Crop": "Rice"
  },
  {
    "Nitrogen": "78",
    "Phosphorus": "42",
    "Potassium": "42",
    "Temperature": 20.13,
    "Humidity": 81.605,
    "pH_Value": 7.628,
    "Rainfall": 262.717,
    "Crop": "Rice"
  }
]
```

---

### `archive (17)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (18)\Crop_Recm_Data.csv`
- **Dimensions**: 10470 rows × 10 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": 32.0,
    "P": 141.0,
    "K": 204.0,
    "temperature": 8.826,
    "humidity": 82.898,
    "ph": 5.537,
    "rainfall": 67.236,
    "label": "grapes",
    "Medicine": "Copper Fungicide",
    "Medicine_Use": "treats bacterial and fungal diseases."
  },
  {
    "N": 14.744,
    "P": 136.13,
    "K": 201.825,
    "temperature": 8.826,
    "humidity": 88.034,
    "ph": 6.682,
    "rainfall": 85.986,
    "label": "apple",
    "Medicine": "Copper Fungicide",
    "Medicine_Use": "treats bacterial and fungal diseases."
  },
  {
    "N": 90.562,
    "P": 48.131,
    "K": 141.493,
    "temperature": 8.828,
    "humidity": 30.11,
    "ph": 5.501,
    "rainfall": 291.742,
    "label": "chickpea",
    "Medicine": "Foliar Fungicide (Mancozeb)",
    "Medicine_Use": "prevents leaf spots and blights."
  },
  {
    "N": 46.547,
    "P": 17.982,
    "K": 197.573,
    "temperature": 8.828,
    "humidity": 91.032,
    "ph": 7.153,
    "rainfall": 244.363,
    "label": "apple",
    "Medicine": "Copper Fungicide",
    "Medicine_Use": "treats bacterial and fungal diseases."
  },
  {
    "N": 129.446,
    "P": 29.259,
    "K": 13.022,
    "temperature": 8.829,
    "humidity": 55.442,
    "ph": 3.589,
    "rainfall": 175.051,
    "label": "coffee",
    "Medicine": "Systemic Fungicide",
    "Medicine_Use": "Fungicide controls Coffee Leaf Rust."
  }
]
```

---

### `archive (19)\data_core.csv`
- **Dimensions**: 8000 rows × 9 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `Crop Type, Fertilizer Name`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: barley, cotton, ground nuts, maize, millets, oil seeds, paddy, pulses, sugarcane, tobacco, wheat
- **First 5 Sample Rows**:

```json
[
  {
    "Temparature": 26.0,
    "Humidity": 52.0,
    "Moisture": 38.0,
    "Soil Type": "Sandy",
    "Crop Type": "Maize",
    "Nitrogen": "37",
    "Potassium": "0",
    "Phosphorous": "0",
    "Fertilizer Name": "Urea"
  },
  {
    "Temparature": 29.0,
    "Humidity": 52.0,
    "Moisture": 45.0,
    "Soil Type": "Loamy",
    "Crop Type": "Sugarcane",
    "Nitrogen": "12",
    "Potassium": "0",
    "Phosphorous": "36",
    "Fertilizer Name": "DAP"
  },
  {
    "Temparature": 34.0,
    "Humidity": 65.0,
    "Moisture": 62.0,
    "Soil Type": "Black",
    "Crop Type": "Cotton",
    "Nitrogen": "7",
    "Potassium": "9",
    "Phosphorous": "30",
    "Fertilizer Name": "14-35-14"
  },
  {
    "Temparature": 32.0,
    "Humidity": 62.0,
    "Moisture": 34.0,
    "Soil Type": "Red",
    "Crop Type": "Tobacco",
    "Nitrogen": "22",
    "Potassium": "0",
    "Phosphorous": "20",
    "Fertilizer Name": "28-28"
  },
  {
    "Temparature": 28.0,
    "Humidity": 54.0,
    "Moisture": 46.0,
    "Soil Type": "Clayey",
    "Crop Type": "Paddy",
    "Nitrogen": "35",
    "Potassium": "0",
    "Phosphorous": "0",
    "Fertilizer Name": "Urea"
  }
]
```

---

### `archive (2)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (22)\Fertilizer.csv`
- **Dimensions**: 1843 rows × 6 columns
- **Feeds Agents**: `CropGrowthAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `Crop`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: almond nut, aniseed, apple, apricot, arecanut, asafoetida, ash gourd, banana, barley(jav), bay leaf, beetroot, bitter gourd, black eyed beans( chawli), black gram, black pepper...
- **First 5 Sample Rows**:

```json
[
  {
    "Unnamed: 0": "0",
    "Crop": "Rice",
    "N": "80",
    "P": "40",
    "K": "40",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "1",
    "Crop": "Jowar(Sorghum)",
    "N": "80",
    "P": "40",
    "K": "40",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "2",
    "Crop": "Barley(JAV)",
    "N": "70",
    "P": "40",
    "K": "45",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "3",
    "Crop": "Maize",
    "N": "80",
    "P": "40",
    "K": "20",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "4",
    "Crop": "Ragi( naachnnii)",
    "N": "50",
    "P": "40",
    "K": "20",
    "pH": 5.5
  }
]
```

---

### `archive (27)\Fertilizer.csv`
- **Dimensions**: 1843 rows × 6 columns
- **Feeds Agents**: `CropGrowthAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `Crop`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: almond nut, aniseed, apple, apricot, arecanut, asafoetida, ash gourd, banana, barley(jav), bay leaf, beetroot, bitter gourd, black eyed beans( chawli), black gram, black pepper...
- **First 5 Sample Rows**:

```json
[
  {
    "Unnamed: 0": "0",
    "Crop": "Rice",
    "N": "80",
    "P": "40",
    "K": "40",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "1",
    "Crop": "Jowar(Sorghum)",
    "N": "80",
    "P": "40",
    "K": "40",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "2",
    "Crop": "Barley(JAV)",
    "N": "70",
    "P": "40",
    "K": "45",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "3",
    "Crop": "Maize",
    "N": "80",
    "P": "40",
    "K": "20",
    "pH": 5.5
  },
  {
    "Unnamed: 0": "4",
    "Crop": "Ragi( naachnnii)",
    "N": "50",
    "P": "40",
    "K": "20",
    "pH": 5.5
  }
]
```

---

### `archive (3)\soil_with_crop_recommendations.csv`
- **Dimensions**: 3400 rows × 20 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label, Crop1, Crop2, Crop3`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - `Timestamp`: 64.71% missing
  - `Plant_ID`: 64.71% missing
  - `Soil_Moisture`: 64.71% missing
  - `Ambient_Temperature`: 64.71% missing
  - `Light_Intensity`: 64.71% missing
  - `Chlorophyll_Content`: 64.71% missing
  - `Electrochemical_Signal`: 64.71% missing
  - `Plant_Health_Status`: 64.71% missing
  - `rainfall`: 35.29% missing
  - `label`: 35.29% missing
- **Crops Present**: 1.0, 10.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, apple, banana, barley, blackgram, chickpea...
- **First 5 Sample Rows**:

```json
[
  {
    "Timestamp": "54:53.4",
    "Plant_ID": 1.0,
    "Soil_Moisture": 27.521,
    "Ambient_Temperature": 22.24,
    "Soil_Temperature": 21.9,
    "Humidity": 55.292,
    "Light_Intensity": 556.173,
    "Soil_pH": 5.582,
    "Nitrogen_Level": 10.004,
    "Phosphorus_Level": 45.807,
    "Potassium_Level": 39.076,
    "Chlorophyll_Content": 35.703,
    "Electrochemical_Signal": 0.941,
    "Plant_Health_Status": "High Stress",
    "rainfall": "null",
    "label": "null",
    "Soil_Type": "Slightly Acidic",
    "Crop1": "Rice",
    "Crop2": "Maize",
    "Crop3": "Groundnut"
  },
  {
    "Timestamp": "54:53.4",
    "Plant_ID": 1.0,
    "Soil_Moisture": 14.836,
    "Ambient_Temperature": 21.707,
    "Soil_Temperature": 18.681,
    "Humidity": 63.949,
    "Light_Intensity": 596.137,
    "Soil_pH": 7.136,
    "Nitrogen_Level": 30.713,
    "Phosphorus_Level": 25.394,
    "Potassium_Level": 17.945,
    "Chlorophyll_Content": 27.993,
    "Electrochemical_Signal": 0.165,
    "Plant_Health_Status": "High Stress",
    "rainfall": "null",
    "label": "null",
    "Soil_Type": "Neutral",
    "Crop1": "Wheat",
    "Crop2": "Barley",
    "Crop3": "Sugarcane"
  },
  {
    "Timestamp": "54:53.4",
    "Plant_ID": 1.0,
    "Soil_Moisture": 17.086,
    "Ambient_Temperature": 21.181,
    "Soil_Temperature": 15.393,
    "Humidity": 67.838,
    "Light_Intensity": 591.125,
    "Soil_pH": 5.657,
    "Nitrogen_Level": 29.337,
    "Phosphorus_Level": 27.574,
    "Potassium_Level": 35.707,
    "Chlorophyll_Content": 43.646,
    "Electrochemical_Signal": 1.082,
    "Plant_Health_Status": "High Stress",
    "rainfall": "null",
    "label": "null",
    "Soil_Type": "Slightly Acidic",
    "Crop1": "Rice",
    "Crop2": "Maize",
    "Crop3": "Groundnut"
  },
  {
    "Timestamp": "54:53.4",
    "Plant_ID": 1.0,
    "Soil_Moisture": 15.336,
    "Ambient_Temperature": 22.593,
    "Soil_Temperature": 22.778,
    "Humidity": 58.191,
    "Light_Intensity": 241.412,
    "Soil_pH": 5.585,
    "Nitrogen_Level": 16.967,
    "Phosphorus_Level": 26.181,
    "Potassium_Level": 26.258,
    "Chlorophyll_Content": 37.838,
    "Electrochemical_Signal": 1.186,
    "Plant_Health_Status": "High Stress",
    "rainfall": "null",
    "label": "null",
    "Soil_Type": "Slightly Acidic",
    "Crop1": "Rice",
    "Crop2": "Maize",
    "Crop3": "Groundnut"
  },
  {
    "Timestamp": "54:53.4",
    "Plant_ID": 1.0,
    "Soil_Moisture": 39.822,
    "Ambient_Temperature": 28.929,
    "Soil_Temperature": 18.101,
    "Humidity": 63.772,
    "Light_Intensity": 444.494,
    "Soil_pH": 5.92,
    "Nitrogen_Level": 10.945,
    "Phosphorus_Level": 37.899,
    "Potassium_Level": 37.654,
    "Chlorophyll_Content": 48.266,
    "Electrochemical_Signal": 1.61,
    "Plant_Health_Status": "High Stress",
    "rainfall": "null",
    "label": "null",
    "Soil_Type": "Slightly Acidic",
    "Crop1": "Rice",
    "Crop2": "Maize",
    "Crop3": "Groundnut"
  }
]
```

---

### `archive (4)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (5)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

### `archive (6)\Crop Recommendation Dataset.xlsx`
- **Dimensions**: 7000 rows × 5 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `Label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: aleovera, apple, arecanut, ashwagandha, bajra, banana, beetroot, blackgram, brinjal, broccoli, button mushrooms, cabbage, capsicum, carrot, cashewnuts...
- **First 5 Sample Rows**:

```json
[
  {
    "Temperature": 20.88,
    "Humidity": 82.003,
    "pH": 6.503,
    "Rainfall": 202.936,
    "Label": "Rice"
  },
  {
    "Temperature": 21.77,
    "Humidity": 80.32,
    "pH": 7.038,
    "Rainfall": 226.656,
    "Label": "Rice"
  },
  {
    "Temperature": 23.004,
    "Humidity": 82.321,
    "pH": 7.84,
    "Rainfall": 263.964,
    "Label": "Rice"
  },
  {
    "Temperature": 26.491,
    "Humidity": 80.158,
    "pH": 6.98,
    "Rainfall": 242.864,
    "Label": "Rice"
  },
  {
    "Temperature": 20.13,
    "Humidity": 81.605,
    "pH": 7.628,
    "Rainfall": 262.717,
    "Label": "Rice"
  }
]
```

---

### `archive (7)\crop_recommendation (1).csv`
- **Dimensions**: 1000 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `crop`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: barley, cotton, maize, rice, soybean, sugarcane, wheat
- **First 5 Sample Rows**:

```json
[
  {
    "N": "102",
    "P": "80",
    "K": "45",
    "temperature": 35.55,
    "humidity": 60.8,
    "ph": 8.32,
    "rainfall": 194.2,
    "crop": "Soybean"
  },
  {
    "N": "92",
    "P": "13",
    "K": "195",
    "temperature": 24.51,
    "humidity": 37.72,
    "ph": 4.7,
    "rainfall": 79.8,
    "crop": "Sugarcane"
  },
  {
    "N": "14",
    "P": "8",
    "K": "32",
    "temperature": 34.39,
    "humidity": 51.52,
    "ph": 7.8,
    "rainfall": 59.12,
    "crop": "Cotton"
  },
  {
    "N": "106",
    "P": "39",
    "K": "0",
    "temperature": 39.11,
    "humidity": 87.03,
    "ph": 6.04,
    "rainfall": 63.19,
    "crop": "Wheat"
  },
  {
    "N": "71",
    "P": "65",
    "K": "146",
    "temperature": 20.09,
    "humidity": 47.93,
    "ph": 6.65,
    "rainfall": 258.54,
    "crop": "Barley"
  }
]
```

---

### `archive (8)\crop_data.csv`
- **Dimensions**: 694 rows × 7 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `CROP`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: aloe vera, amaranth (rajgira), ashwagandha, asparagus, avocado, bamboo, banana, barley, barnyard millet, bittergourd, blackgram, blackpepper, blueberry, bottlegourd, brinjal...
- **First 5 Sample Rows**:

```json
[
  {
    "CROP": "DRAGON FRUIT",
    "N": "100",
    "P": "55",
    "K": "165",
    "PH": 5.7,
    "RAINFALL": 1050.0,
    "TEMP": 32.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "100",
    "P": "60",
    "K": "160",
    "PH": 6.5,
    "RAINFALL": 900.0,
    "TEMP": 32.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "90",
    "P": "30",
    "K": "160",
    "PH": 6.4,
    "RAINFALL": 900.0,
    "TEMP": 31.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "80",
    "P": "40",
    "K": "150",
    "PH": 6.0,
    "RAINFALL": 800.0,
    "TEMP": 30.0
  },
  {
    "CROP": "DRAGON FRUIT",
    "N": "80",
    "P": "45",
    "K": "150",
    "PH": 6.0,
    "RAINFALL": 800.0,
    "TEMP": 34.0
  }
]
```

---

### `archive (9)\Crop_recommendation.csv`
- **Dimensions**: 2200 rows × 8 columns
- **Feeds Agents**: `CropGrowthAgent, WeatherAgent, YieldForecastAgent`
- **Geographic Columns**: `None`
- **Target / Label Columns**: `label`
- **Date Range**: Cross-sectional agronomic observations
- **Missing Value Analysis**:
  - *Clean dataset: 0.00% missing values across all columns.*
- **Crops Present**: apple, banana, blackgram, chickpea, coconut, coffee, cotton, grapes, jute, kidneybeans, lentil, maize, mango, mothbeans, mungbean...
- **First 5 Sample Rows**:

```json
[
  {
    "N": "90",
    "P": "42",
    "K": "43",
    "temperature": 20.88,
    "humidity": 82.003,
    "ph": 6.503,
    "rainfall": 202.936,
    "label": "rice"
  },
  {
    "N": "85",
    "P": "58",
    "K": "41",
    "temperature": 21.77,
    "humidity": 80.32,
    "ph": 7.038,
    "rainfall": 226.656,
    "label": "rice"
  },
  {
    "N": "60",
    "P": "55",
    "K": "44",
    "temperature": 23.004,
    "humidity": 82.321,
    "ph": 7.84,
    "rainfall": 263.964,
    "label": "rice"
  },
  {
    "N": "74",
    "P": "35",
    "K": "40",
    "temperature": 26.491,
    "humidity": 80.158,
    "ph": 6.98,
    "rainfall": 242.864,
    "label": "rice"
  },
  {
    "N": "78",
    "P": "42",
    "K": "42",
    "temperature": 20.13,
    "humidity": 81.605,
    "ph": 7.628,
    "rainfall": 262.717,
    "label": "rice"
  }
]
```

---

## 3. Crop Registry Cross-Check (40 Target Crops vs Datasets)

### Directly Grounded Crops (39/40)
The following crops are directly represented in the local datasets with nutrient, temperature, and yield characteristics:

`rice`, `wheat`, `maize`, `barley`, `sorghum`, `pearl millet`, `finger millet`, `sugarcane`, `onion`, `garlic`, `turmeric`, `ginger`, `carrot`, `radish`, `beetroot`, `potato`, `sunflower`, `mustard`, `tomato`, `chili`, `brinjal`, `cotton`, `tea`, `groundnut`, `soybean`, `chickpea`, `lentil`, `pigeon pea`, `green gram`, `black gram`, `cucumber`, `bottle gourd`, `bitter gourd`, `pumpkin`, `watermelon`, `grape`, `banana`, `jute`, `sesame`

### Parametrically Extrapolated Crops (1/40)
The following crops inherit calibrated archetype parameters (growth duration, water requirement, canopy density) based on their biological archetype family:

`okra`

## 4. Agent Fallback Strategy & Real Data Policy

As mandated by project constraints, **no data is ever fabricated**:
1. **Pest & Disease**: Datasets lack continuous daily pest trap records. Therefore, `PestDiseaseAgent` implements Tamil Nadu Agricultural University (TNAU) agrometeorological thresholds: High risk triggers when relative humidity > 70% and temperatures sit between 20°C and 30°C for >= 48 hours.
2. **Live Weather**: Local datasets provide training distributions. For real-time field coordinates, `NASAPowerClient` acts as the verified live weather source (parameters: `T2M`, `PRECTOTCORR`, `RH2M`). If offline or rate-limited, it falls back to the local empirical seasonal mean tagged with `source: EXTERNAL_FALLBACK`.
3. **Yield Forecasting**: Monte Carlo simulation draws N=1000 empirical samples around the calibrated mean yield derived from `data_core.csv` and `crop_data.csv`.

## 5. Preprocessing & Ingestion Plan

1. **Schema Renaming**: All datasets ingest into the standardized `FieldRecord` model (`date`, `temperature`, `rainfall`, `humidity`, `soil_moisture`, `historical_yield`).
2. **Missing-Value Imputation**: Forward-fill for continuous time-series, median imputation per crop type for nutrient values.
3. **Z-Score Normalization**: Continuous sensor indicators normalized via $(x - \mu) / \sigma$ for agent anomaly detection.
4. **Data Quality Engine**: Evaluates every field input for missing values (>20% penalty), outliers ($|z| > 3$), staleness (>7 days old), and internal consistency (e.g. soil moisture > 100% or negative rainfall).
