import os
import joblib
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

model = joblib.load(os.path.join(MODELS_DIR, "severity_model.joblib"))
preprocessor = joblib.load(os.path.join(MODELS_DIR, "preprocessor.joblib"))

sample_data = pd.DataFrame([
    {
        'road_type': 'highway',
        'weather': 'rain',
        'visibility': 'low',
        'traffic_density': 'high',
        'traffic_signal': '0',
        'is_weekend': '1',
        'is_peak_hour': '1',
        'hour': 21,
        'lanes': 4,
        'temperature': 24.0,
        'vehicles_involved': 3
    },
    {
        'road_type': 'urban',
        'weather': 'clear',
        'visibility': 'high',
        'traffic_density': 'low',
        'traffic_signal': '1',
        'is_weekend': '0',
        'is_peak_hour': '0',
        'hour': 11,
        'lanes': 2,
        'temperature': 28.0,
        'vehicles_involved': 1
    }
])

X_proc = preprocessor.transform(sample_data)
probs = model.predict_proba(X_proc)
preds = model.predict(X_proc)

label_map = {0: 'Minor', 1: 'Major', 2: 'Fatal'}
for i, row in sample_data.iterrows():
    print(f"\n--- Scenario {i+1} ({row['road_type']}, weather: {row['weather']}, visibility: {row['visibility']}) ---")
    print(f"Predicted Severity: {label_map[preds[i]]}")
    print(f"Probabilities: P(Minor)={probs[i][0]:.3f}, P(Major)={probs[i][1]:.3f}, P(Fatal)={probs[i][2]:.3f}")
