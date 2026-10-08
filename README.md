# AI-Based Road Accident Risk & Severity Assessment for Indian Roads

> **Real ML · Real Indian Data · Real Roads · No Fake Data · No Paid API Keys**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61dafb?logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178c6?logo=typescript)](https://typescriptlang.org)
[![Leaflet](https://img.shields.io/badge/Leaflet-OpenStreetMap-1a73e8?logo=leaflet)](https://leafletjs.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## What This Project Does

This system analyzes any Indian highway route and shows a **color-coded risk map** based on:

- 24,350 **real Indian accident records** with GPS coordinates
- **AI/ML model** (Balanced Random Forest) predicting accident severity
- **Live weather** at each route segment (Open-Meteo API)
- **Real OSRM road routing** (not straight lines)
- **SHAP Explainability** — shows WHY a segment is high risk

**Example output:**
> *"⚠ HIGH RISK AHEAD — 650m | Risk Score: 71/100 | 3 fatal accidents historically recorded nearby | Rain detected"*

---

## Live Demo Screenshots

| Mumbai → Pune Risk Map | GPS Drive Simulation | Segment Risk Breakdown |
|------------------------|----------------------|------------------------|
| *(Route with colored segments)* | *(Real-time drive warnings)* | *(SHAP explainability)* |

---

## Key Features

- **Interactive OSM Map** — Real road network, no Carto/Google API key needed
- **0–100 Risk Score** per route segment (5-factor transparent formula)
- **AI Severity Prediction** — Minor / Major / Fatal (Random Forest, Macro F1: 0.3260)
- **SHAP Explainability** — Know exactly WHY a zone is dangerous
- **Live Weather Integration** — Open-Meteo API at segment GPS coordinates
- **DBSCAN Hotspot Clustering** — 130 verified accident blackspots
- **GPS Drive Simulation** — "Drive Route" mode with real-time risk alerts
- **7 Preset Indian Corridors** — Mumbai→Pune, Delhi→Jaipur, Chennai→Hyderabad, and more
- **Historical Data Integrity** — Never fabricates data; shows "unavailable" where real data is absent

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, FastAPI, Uvicorn |
| **ML / AI** | scikit-learn, imbalanced-learn, XGBoost, SHAP |
| **Spatial** | scipy BallTree (Haversine), DBSCAN |
| **Routing** | OSRM (router.project-osrm.org) — free |
| **Geocoding** | Nominatim (OpenStreetMap) — free |
| **Weather** | Open-Meteo API — free |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS v4 |
| **Map** | Leaflet.js + OpenStreetMap tiles — free, no API key |

---

## Model Accuracy

| Model | Accuracy | Macro F1 | Decision |
|-------|----------|----------|----------|
| **Random Forest (Balanced)** | 39.27% | **0.3260** | ✅ Selected |
| Gradient Boosting | 53.83% | 0.2543 | ❌ Majority-biased |
| XGBoost | 54.05% | 0.2531 | ❌ Majority-biased |

> **Why 39% over 54%?** Gradient Boosting/XGBoost predict "Minor" for almost everything (55% of data is Minor). They never detect Fatal accidents. Random Forest (Balanced) uses `class_weight='balanced'` to fairly detect all 3 severity classes — critical for a road safety system.

---

## Risk Score Formula

```
Total Risk (0–100) =
    Historical Accident Density   (0–30 pts)   — from 20,000 GPS accident points
  + ML Severity Probability       (0–30 pts)   — P(Fatal) × 30 + P(Major) × 15
  + Live Weather                  (0–15 pts)   — rain/fog/wind from Open-Meteo
  + Road Geometry                 (0–15 pts)   — curve detection from GPS polyline
  + Temporal Factor               (0–10 pts)   — night/weekend multiplier

LOW = 0–30 (Green)  |  MEDIUM = 31–55 (Amber)  |  HIGH = 56–75 (Orange)  |  VERY HIGH = 76–100 (Red)
```

---

## Dataset Sources

| File | Records | Source |
|------|---------|--------|
| `data/indian_roads_dataset.csv` | 20,000 | [Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025](https://github.com/Prashantsundar) |
| `data/accident_prediction_india.csv` | 3,000 | [rahul-saha18/India-Road-Accident-EDA](https://github.com/rahul-saha18) |
| `data/ndap_accident_dataset.csv` | 1,350 | [NITI Aayog NDAP](https://ndap.gov.in) — Official Government |

All data is **real, verified Indian road accident records**. Zero synthetic data.

---

## Project Structure

```
major-project/
├── backend/
│   ├── main.py              # FastAPI app (5 endpoints)
│   ├── spatial_index.py     # BallTree spatial index + DBSCAN hotspots
│   ├── risk_engine.py       # 0-100 risk scorer + SHAP explainability
│   ├── weather_client.py    # Open-Meteo live weather client
│   └── osrm_client.py       # OSRM routing + Nominatim geocoding
├── frontend/
│   └── src/
│       ├── App.tsx           # Main React app + GPS simulation
│       └── components/
│           ├── MapViewer.tsx # Leaflet + OSM map + risk route
│           ├── InfoPanel.tsx # Dashboard, presets, SHAP cards
│           └── ModelInfoModal.tsx
├── data/                    # Real Indian accident CSV files
├── models/                  # Trained ML model (.joblib files)
├── scripts/                 # Training + testing scripts
├── docs/                    # Documentation
├── HOW_TO_RUN.md            # Run guide
├── HOW_TO_INCREASE_ACCURACY.md
└── NOTES_AND_DATASET_GUIDE.md
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

### 4. Start backend (Terminal 1)

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### 5. Start frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

### 6. Open in browser

```
http://localhost:5173/
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health, dataset stats |
| `/api/hotspots` | GET | All 130 accident hotspots |
| `/api/model-info` | GET | ML model accuracy + metrics |
| `/api/route` | POST | Compute route risk assessment |
| `/api/simulate-gps` | POST | GPS position risk lookup |

---

## Preset Corridors

- Mumbai → Pune (NH-48)
- Delhi → Jaipur (NH-48)
- Bengaluru → Chennai (NH-44)
- Chennai → Hyderabad (NH-65)
- Kolhapur → Bengaluru
- Kolkata → Bhubaneswar (NH-16)
- Delhi → Mumbai

---

## Limitations

- Historical GPS data covers 7 Indian states (MH, DL, KA, TN, TS, PB, WB)
- Segments outside GPS coverage show "Historical data unavailable" (not fabricated)
- OSRM public API may be rate-limited occasionally (fallback routing auto-activates)
- ML model accuracy is 39.27% — improvement roadmap in `HOW_TO_INCREASE_ACCURACY.md`

---

## Future Scope

- Add MoRTH / iRAD datasets (100,000+ records, all 28+ states)
- SMOTE oversampling + Optuna hyperparameter tuning
- Ensemble model (RF + XGBoost + LightGBM)
- Mobile-responsive PWA
- Real-time GPS from device location
- Official NHAI black spot integration

---

## License

MIT License — Free to use, modify, and distribute.

---

## Author

Built as a Final Year B.E./B.Tech Computer Science Project.

**Project:** AI-Based Road Accident Risk and Severity Assessment with Explainable Route Risk Mapping for Indian Roads
