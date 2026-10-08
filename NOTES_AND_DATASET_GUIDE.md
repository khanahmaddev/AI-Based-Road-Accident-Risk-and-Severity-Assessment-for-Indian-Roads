# PROJECT NOTES — Everything Saved
# AI-Based Road Accident Risk and Severity Assessment for Indian Roads
# Last Updated: 2026-10-08 23:07 IST

==============================================================
SECTION 1: COMPLETE PROJECT NOTES (EVERYTHING WE DID)
==============================================================

---

## What This Project Is

Name: AI-Based Road Accident Risk and Severity Assessment for Indian Roads
Title (Professor-safe version):
    "AI-Based Road Accident Risk and Severity Assessment with Explainable Route Risk Mapping"

Core Idea:
    NOT "predicting where an accident WILL happen"
    YES "showing HIGH-RISK AREAS on route based on historical data + ML + live conditions"

Example output to user:
    "High-risk area ahead — 650m (3 fatal accidents historically recorded nearby)"

---

## Files Created in This Project (All 3 Phases)

Phase 1 — Data and ML:
    data/indian_roads_dataset.csv          (20,000 real GPS accident records, 2.7MB)
    data/accident_prediction_india.csv     (3,000 records, 32 States/UTs, 422KB)
    data/ndap_accident_dataset.csv         (1,350 NITI Aayog NDAP official records, 119KB)
    models/severity_model.joblib           (trained Random Forest Classifier)
    models/preprocessor.joblib            (scikit-learn ColumnTransformer)
    models/model_metadata.json             (accuracy, F1, label mapping)
    scripts/download_datasets.py           (downloads all 3 datasets)
    scripts/train_severity_models.py       (trains RF, GB, XGB, compares, saves best)
    scripts/test_inference.py              (verifies model probabilities)
    docs/dataset_and_models.md             (dataset schema + evaluation metrics)

Phase 2 — Backend + Frontend:
    backend/__init__.py
    backend/main.py                        (FastAPI, 5 endpoints)
    backend/spatial_index.py              (BallTree spatial index + DBSCAN 130 hotspots)
    backend/risk_engine.py               (0-100 risk scorer + SHAP)
    backend/weather_client.py            (Open-Meteo live weather)
    backend/osrm_client.py               (OSRM routing + Nominatim + fallback)
    frontend/src/App.tsx                  (main React app + GPS simulation)
    frontend/src/components/MapViewer.tsx (Leaflet OSM map + colored route)
    frontend/src/components/InfoPanel.tsx (dashboard, presets, SHAP cards)
    frontend/src/components/ModelInfoModal.tsx (ML metrics modal)
    frontend/src/types.ts                 (TypeScript interfaces)
    frontend/src/index.css               (TailwindCSS + Leaflet styles)
    frontend/vite.config.ts              (Vite + API proxy)
    scripts/test_pipeline.py             (end-to-end test)
    scripts/test_api_endpoints.py        (API tests — all passed)

Phase 3 — Browser Testing + Map Fix:
    frontend/src/components/MapViewer.tsx (UPDATED: Carto removed, OSM added)
    frontend/src/index.css               (UPDATED: Google Maps light style)

Documentation Files Created:
    PROJECT_STATUS.md                    (main status — all phases complete)
    HOW_TO_RUN.md                       (step-by-step run guide)
    HOW_TO_INCREASE_ACCURACY.md         (7 methods to improve accuracy)
    DOCUMENTATION_AND_DIAGRAM_PROMPTS.md (19 AI prompts for docs and diagrams)
    CHANGELOG.md                         (milestone log)
    docs/progress.md                     (detailed step-by-step tracker)
    NOTES_AND_DATASET_GUIDE.md          (this file — everything saved)

---

## Key Numbers to Remember

| Metric | Value |
|--------|-------|
| Total Accident Records | 24,350 |
| GPS-tagged Records | 20,000 |
| Indian States/UTs Covered | 32 (accident_prediction_india.csv) |
| GPS Coverage States | 7 (MH, DL, KA, TN, TS, PB, WB) |
| DBSCAN Hotspots Found | 130 |
| ML Model Accuracy | 39.27% |
| ML Macro F1 Score | 0.3260 |
| Backend API Endpoints | 5 |
| Preset Corridors | 7 |
| Mumbai-Pune segments | 15 |
| Mumbai-Pune distance | 147.7 km |
| Delhi-Jaipur distance | 297.6 km |
| Chennai-Hyderabad segments | 42 |
| Chennai-Hyderabad distance | 627.1 km |
| Risk Score Range | 0 to 100 |

---

## Tech Stack Summary

Backend:
    Python 3.10+
    FastAPI + Uvicorn
    scikit-learn (Random Forest, preprocessing)
    imbalanced-learn (BalancedRandomForestClassifier)
    XGBoost
    SHAP (TreeExplainer)
    scipy (BallTree + DBSCAN)
    pandas, numpy
    urllib (OSRM + Nominatim requests)

Frontend:
    React 18 + TypeScript
    Vite 8 (build tool)
    TailwindCSS v4
    Leaflet + react-leaflet
    Lucide React (icons)
    OpenStreetMap tiles (FREE, no API key)

External APIs (all FREE, no key needed):
    router.project-osrm.org    (real road routing)
    nominatim.openstreetmap.org (geocoding)
    api.open-meteo.com          (live weather)
    tile.openstreetmap.org      (map tiles in browser)

---

## Risk Score Formula (Remember This for Viva)

Total Risk (0-100) =
    Historical Density   (0-30 pts)  +
    ML Severity          (0-30 pts)  +
    Live Weather         (0-15 pts)  +
    Road Geometry        (0-15 pts)  +
    Temporal             (0-10 pts)

Tiers:
    0-30   = LOW        (Green)
    31-55  = MEDIUM     (Amber/Yellow)
    56-75  = HIGH       (Orange)
    76-100 = VERY HIGH  (Red)

---

## Why Random Forest over XGBoost (Viva Answer)

XGBoost accuracy: 54.05% but Macro F1 = 0.2531
Random Forest accuracy: 39.27% but Macro F1 = 0.3260

XGBoost predicts "Minor" for almost everything because 55% of data is Minor.
It never detects Fatal accidents.

Random Forest (Balanced) uses class_weight='balanced' which compensates for imbalance.
It fairly detects all 3 classes: Minor, Major, Fatal.

For a SAFETY system, missing Fatal accidents is unacceptable.
That is why we chose Macro F1 as our metric, not raw accuracy.

---

==============================================================
SECTION 2: DATASET CHANGE GUIDE
==============================================================

---

## Q: Can We Change the Dataset to Another Dataset?

YES, 100% POSSIBLE.

The project is built modularly. The dataset is only used in:
    1. scripts/train_severity_models.py    (training the ML model)
    2. backend/spatial_index.py           (loading GPS points for spatial queries)
    3. scripts/download_datasets.py       (downloading the original datasets)

If you change the dataset, you only need to:
    1. Prepare new CSV with correct column format
    2. Retrain the model (run train_severity_models.py)
    3. Rebuild the spatial index (restarts automatically when backend starts)

Frontend, MapViewer, InfoPanel, API endpoints — NOTHING CHANGES.
The risk score formula — NOTHING CHANGES.
The 0-100 scoring system — NOTHING CHANGES.

---

## Required Column Format for New Dataset

For the MAIN GPS dataset (replaces indian_roads_dataset.csv):

REQUIRED COLUMNS:
    latitude          (float)   e.g. 18.5204
    longitude         (float)   e.g. 73.8567
    severity          (string)  values: "Minor" or "Major" or "Fatal"

RECOMMENDED COLUMNS (for better risk scoring):
    road_type         (string)  e.g. "National Highway", "State Road", "Urban"
    weather           (string)  e.g. "Clear", "Rain", "Fog", "Dust"
    time_of_day       (string)  e.g. "Morning", "Afternoon", "Night"
    junction_type     (string)  e.g. "T-junction", "Straight", "Roundabout"
    cause             (string)  e.g. "Over-speeding", "Drunk driving"
    casualties        (int)     e.g. 2
    city              (string)  e.g. "Mumbai"
    state             (string)  e.g. "Maharashtra"
    date              (string)  e.g. "2023-08-15"
    time              (string)  e.g. "22:30"

MINIMUM REQUIRED FOR SPATIAL INDEX: latitude + longitude + severity

---

## Step-by-Step: How to Replace the Dataset

### STEP 1 — Prepare Your New CSV File

Your new CSV must have at minimum:
    latitude, longitude, severity

Save it as: data/my_new_dataset.csv

Example valid row:
    latitude,longitude,severity,road_type,weather,casualties
    18.9220,72.8347,Fatal,National Highway,Rain,2
    28.6139,77.2090,Minor,Urban Road,Clear,0
    13.0827,80.2707,Major,State Road,Fog,1

---

### STEP 2 — Edit the Download Script (optional)

If your dataset comes from a URL, edit scripts/download_datasets.py:

    # Replace the existing download URL for dataset 1
    DATASET_1_URL = "https://your-new-dataset-url.com/data.csv"
    DATASET_1_FILE = "data/my_new_dataset.csv"

Or just copy your CSV file manually into the data/ folder.

---

### STEP 3 — Edit the Training Script

Open scripts/train_severity_models.py and find where datasets are loaded.

CURRENT CODE (look for something like):
    df1 = pd.read_csv('data/indian_roads_dataset.csv')
    df2 = pd.read_csv('data/accident_prediction_india.csv')
    df3 = pd.read_csv('data/ndap_accident_dataset.csv')

CHANGE TO (example with your new dataset):
    df1 = pd.read_csv('data/my_new_dataset.csv')
    # Remove or comment out old datasets if not needed

If your column names are different, add a rename step:
    df1 = df1.rename(columns={
        'Accident_Severity': 'severity',    # rename your column to 'severity'
        'Lat': 'latitude',                  # rename to 'latitude'
        'Lon': 'longitude',                 # rename to 'longitude'
        'Road_Type': 'road_type',           # rename to 'road_type'
    })

---

### STEP 4 — Edit the Spatial Index (if column names differ)

Open backend/spatial_index.py and find where the CSV is loaded.

CURRENT CODE (look for):
    df = pd.read_csv('data/indian_roads_dataset.csv')
    coords = df[['latitude', 'longitude']].values

CHANGE TO:
    df = pd.read_csv('data/my_new_dataset.csv')
    # Rename if needed
    df = df.rename(columns={'Lat': 'latitude', 'Lon': 'longitude'})
    coords = df[['latitude', 'longitude']].values

The spatial index (BallTree) and DBSCAN hotspot detection will work automatically
with any lat/lon data — no other changes needed.

---

### STEP 5 — Retrain the Model

Run:
    cd "c:\major project"
    python scripts/train_severity_models.py

This will:
    - Load your new dataset
    - Train RF, Gradient Boosting, XGBoost
    - Compare Macro F1 scores
    - Save best model to models/severity_model.joblib
    - Save preprocessor to models/preprocessor.joblib
    - Save accuracy info to models/model_metadata.json

---

### STEP 6 — Restart the Backend

Stop the existing backend (Ctrl+C) and restart:

    cd "c:\major project"
    python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

The backend will automatically:
    - Load new model from models/severity_model.joblib
    - Rebuild spatial index from new CSV
    - Recompute DBSCAN hotspots

---

### STEP 7 — Verify It Works

Run the verification tests:
    python scripts/test_inference.py      # check model probabilities
    python scripts/test_pipeline.py       # check end-to-end routing
    python scripts/test_api_endpoints.py  # check all 5 API endpoints

---

## Compatible Dataset Sources (Ready to Use)

These datasets can be used with minimal changes:

| Dataset | Records | GPS | Severity | Source |
|---------|---------|-----|----------|--------|
| Current: indian_roads_dataset.csv | 20,000 | YES | YES | GitHub |
| MoRTH Annual Data | 100,000+ | PARTIAL | YES | data.gov.in |
| iRAD (Integrated Road Accident DB) | Active | YES | YES | irad.nic.in |
| NDAP (more tables) | 5,000+ | NO | YES | ndap.gov.in |
| Kaggle India Road Accidents | 50,000+ | SOME | YES | kaggle.com |
| US NHTSA (if comparison needed) | 500,000+ | YES | YES | nhtsa.gov |
| UK Road Safety Data | 200,000+ | YES | YES | data.gov.uk |

For non-Indian datasets: The risk engine, map, and routing still work,
but the BallTree spatial index will show accident data from that region only.
The map will still show Indian routes (OSRM routes in India by default).

---

## What CANNOT Be Changed Easily

These are hardcoded and would need more work to change:

| Component | What's Fixed | Effort to Change |
|-----------|-------------|-----------------|
| Severity classes | Minor, Major, Fatal (exactly these 3) | Medium — retrain model with new labels |
| Risk score formula | 5 factors, fixed weights | Easy — edit backend/risk_engine.py |
| Preset corridors | 7 Indian cities | Easy — edit InfoPanel.tsx |
| Map region | India (OSRM routes in India) | Medium — OSRM works globally but UI is India-focused |
| ML model type | Random Forest as default | Easy — change in train_severity_models.py |

---

## Summary

Can dataset be changed?   YES — 100% possible
Files to edit:            scripts/train_severity_models.py + backend/spatial_index.py
Retraining needed:        YES — python scripts/train_severity_models.py
Backend restart needed:   YES — python -m uvicorn backend.main:app ...
Frontend changes needed:  NO — zero frontend changes
API changes needed:       NO — zero API changes
Time to switch dataset:   30 minutes to 2 hours depending on data cleaning needed

==============================================================
Last Updated: 2026-10-08 23:07 IST
==============================================================
