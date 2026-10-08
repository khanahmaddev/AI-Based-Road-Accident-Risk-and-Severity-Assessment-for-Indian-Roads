# Dataset & Model Training Report

## 1. Real Indian Datasets Acquired

### Primary Geospatial Dataset: `data/indian_roads_dataset.csv`
- **Total Records:** 20,000
- **Geographic Coverage:** India (Maharashtra, Punjab, Tamil Nadu, Delhi, Karnataka, Telangana, West Bengal - covering major inter-city routes: Delhi, Mumbai, Pune, Bengaluru, Hyderabad, Chennai, Kolkata, Chandigarh).
- **Coordinates:** Exact GPS (`latitude`: 12.80 to 30.79, `longitude`: 72.70 to 88.49).
- **Target Variable:** `accident_severity` with 3 levels:
  - `minor`: 11,025 records (55.1%)
  - `major`: 5,988 records (29.9%)
  - `fatal`: 2,987 records (14.9%)
- **Features:** `road_type`, `lanes`, `traffic_signal`, `weather`, `visibility`, `temperature`, `traffic_density`, `cause`, `vehicles_involved`, `casualties`, `hour`, `day_of_week`, `is_weekend`, `is_peak_hour`.

### Supplementary Pan-India Dataset: `data/accident_prediction_india.csv`
- **Total Records:** 3,000
- **Coverage:** 32 Indian States and Union Territories across India.
- **Features:** Road conditions (Wet, Under Construction, Dry), Road geometry (Bridge, Curve, Straight Road), Lighting, Speed Limits, Driver Demographics.

### Official Government Benchmark: `data/ndap_accident_dataset.csv`
- **Total Records:** 1,350
- **Source:** NITI Aayog National Data & Analytics Platform (NDAP).
- **Coverage:** Aggregated statistics for Indian cities and states.

---

## 2. Actual Machine Learning Evaluation Metrics

Models evaluated on an 80/20 stratified split (4,000 test records):

| Metric | Random Forest (Balanced) | Gradient Boosting | XGBoost |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 39.27% | 53.83% | 54.05% |
| **Macro Precision** | 0.3271 | 0.3804 | 0.3834 |
| **Macro Recall** | 0.3268 | 0.3312 | 0.3319 |
| **Macro F1-Score** | **0.3260** | 0.2543 | 0.2531 |
| **Weighted F1-Score** | 0.4001 | 0.4033 | 0.4033 |

### Confusion Matrix (Rows = Actual [Minor, Major, Fatal], Cols = Predicted)

#### Random Forest (Balanced):
```
[[1084,  730,  391],   (Minor:  1084 correct)
 [ 606,  389,  203],   (Major:   389 correct)
 [ 303,  196,   98]]   (Fatal:    98 correct)
```
*Note: Gradient Boosting and XGBoost heavily overfit to predicting the majority class (Minor: >2100 predictions), yielding nearly 0 Fatal detections. Random Forest with balanced class weighting was chosen as the operational baseline because it maintains predictive coverage across all three severity tiers.*

---

## 3. Model Output & Probability Engine

The trained model outputs exact probability distributions:
- $P(\text{Minor})$
- $P(\text{Major})$
- $P(\text{Fatal})$

Where:
$$\sum P(c) = 1.0$$

These probabilities feed into the route-segment risk engine:
$$\text{Severity Risk Score} = 100 \times \left(0.25 \cdot P(\text{Minor}) + 0.60 \cdot P(\text{Major}) + 1.00 \cdot P(\text{Fatal})\right)$$

---

## 4. Saved Artifacts
- Model: `models/severity_model.joblib`
- Feature Preprocessor: `models/preprocessor.joblib`
- Metadata: `models/model_metadata.json`
