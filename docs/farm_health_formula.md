# Farm Health Index (FHI) Mathematical Specification

The **Farm Health Index (FHI)** is an explainable composite metric (scale $0-100$) synthesizing biological vitality, hydrological suitability, pest pathogen pressure, and climatic volatility into a single operational gauge.

---

## 1. Weighted Formulation

$$\text{FHI} = 0.30 \cdot H_{\text{crop}} + 0.25 \cdot H_{\text{soil}} + 0.25 \cdot H_{\text{pest}} + 0.20 \cdot H_{\text{climate}}$$

Where:
- $H_{\text{crop}}$: **Crop Health Index (30%)** — Derived from vegetative growth stage progression and biomass confidence:
  $$H_{\text{crop}} = \text{clip}\left(100 \cdot C_{\text{growth}}, 20, 100\right)$$
- $H_{\text{soil}}$: **Water & Soil Health Index (25%)** — Quantifies root-zone moisture saturation relative to agronomic thresholds:
  $$H_{\text{soil}} = \begin{cases} 95, & 45\% \le \theta \le 75\% \quad (\text{Optimal}) \\ 75, & 30\% \le \theta < 45\% \lor 75\% < \theta \le 85\% \quad (\text{Mild Stress}) \\ 45, & \text{otherwise} \quad (\text{Severe Stress}) \end{cases}$$
- $H_{\text{pest}}$: **Biosecurity / Pest Health Index (25%)** — Inverted risk score indicating crop protection margin:
  $$H_{\text{pest}} = \text{clip}\left(100 \cdot (1 - R_{\text{pest}}), 10, 100\right)$$
- $H_{\text{climate}}$: **Climatic Stability Index (20%)** — Evaluates microclimate thermal anomalies and precipitation deviations:
  $$H_{\text{climate}} = \begin{cases} 35, & \text{Extreme Weather Hazard} \\ 55, & \text{High Thermal Risk} \\ 78, & \text{Moderate Risk} \\ 92, & \text{Favorable Microclimate} \end{cases}$$

---

## 2. Classification Thresholds

| FHI Score Range | Operational Status | Dashboard Indicator | Recommended Action |
| :--- | :--- | :--- | :--- |
| **80 – 100** | **OPTIMAL** | Vibrant Green (`#4ADE80`) | Maintain scheduled baseline irrigation and nutrition. |
| **60 – 79** | **VIGOROUS** | Soft Cyan (`#38BDF8`) | Routine monitoring; microclimate anomalies under control. |
| **40 – 59** | **STRESSED** | Amber Warning (`#F59E0B`) | Implement conflict-resolved advisory (e.g. adjust irrigation). |
| **0 – 39** | **CRITICAL** | Crimson Alert (`#F43F5E`) | Immediate field intervention required (drainage, biocides). |

---

## 3. Data Grounding & Provenance
Every sub-index is traced to concrete field sensors or meteorological feeds. No sub-score is fabricated or randomized without an explicit audit trail.
