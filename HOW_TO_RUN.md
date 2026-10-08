# How to Run — AI Road Accident Risk Assessment (Indian Roads)

> **Project:** AI-Based Road Accident Risk and Severity Assessment for Indian Roads
> **Coverage:** All India — National Coverage
> **Stack:** FastAPI (Python) + React + TypeScript + Leaflet + OpenStreetMap

---

## Prerequisites

| Tool | Minimum Version | Check Command |
|------|-----------------|---------------|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |

---

## Step-by-Step: Running the Project

### STEP 1 — Install Python Dependencies

```bash
cd "c:\major project"
pip install -r requirements.txt
```

### STEP 2 — Install Frontend Dependencies

```bash
cd "c:\major project\frontend"
npm install
```

### STEP 3 — Start the Backend Server (Terminal 1)

```bash
cd "c:\major project"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### STEP 4 — Start the Frontend Dev Server (Terminal 2)

```bash
cd "c:\major project\frontend"
npm run dev
```

Expected output:
```
VITE ready  =>  http://localhost:5173/
```

### STEP 5 — Open in Browser

```
http://localhost:5173/
```

The map will auto-load Mumbai to Pune corridor with:
- Real OpenStreetMap tiles (NO API key needed)
- Color-coded route segments by risk level
- Real Indian accident pins and DBSCAN hotspot circles
- Live weather integration via Open-Meteo
- GPS simulation / Drive Route mode

---

## Using the Application

| Feature | How to Use |
|---------|------------|
| Route Assessment | Enter origin + destination, click Assess Route Risk |
| Preset Corridors | Click any preset: Mumbai-Pune, Delhi-Jaipur, Chennai-Hyderabad, etc. |
| Accident Pins | Toggle Accident Pins button |
| Hotspots | Toggle Hotspots button |
| GPS Simulation | Click Drive Route for real-time risk warnings |
| Segment Details | Click any segment on map or list |
| Model Metrics | Click Metrics button (top-right of panel) |

---

## API Endpoints

Backend at: http://127.0.0.1:8000

| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/health | GET | Health check, dataset stats |
| /api/hotspots | GET | 130 accident hotspots |
| /api/model-info | GET | ML model accuracy |
| /api/route | POST | Route risk assessment |
| /api/simulate-gps | POST | GPS position risk |

---

## Automated Tests

```bash
cd "c:\major project"
python scripts/test_inference.py      # ML model probabilities
python scripts/test_pipeline.py       # Full route pipeline
python scripts/test_api_endpoints.py  # All 5 API endpoints
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | pip install -r requirements.txt |
| Backend crash | Check data/ and models/ folders exist |
| Map blank/white | Check internet (OSM tiles, free, no key) |
| Route API error | OSRM fallback activates automatically |
| Vite not found | npm install inside frontend/ folder |
| Port 8000 busy | netstat -ano then taskkill /PID XXXX /F |

---

## Model Accuracy

| Model | Accuracy | Macro F1 | Decision |
|-------|----------|----------|----------|
| Random Forest (Balanced) | 39.27% | 0.3260 | SELECTED — catches Fatal accidents |
| Gradient Boosting | 53.83% | 0.2543 | Rejected — biased to Minor only |
| XGBoost | 54.05% | 0.2531 | Rejected — biased to Minor only |

WHY 39% over 54%?
Random Forest is selected because Macro F1 = 0.3260 means it fairly detects
all three severity classes (Minor, Major, Fatal). Gradient Boosting/XGBoost
predict "Minor" for almost everything (55% of data IS Minor) — making them
useless for detecting Fatal accidents in a safety system.

---

## Dataset Sources

| File | Records | Source |
|------|---------|--------|
| data/indian_roads_dataset.csv | 20,000 | Prashantsundar/Indian-Road-Accident-Dataset (GitHub) |
| data/accident_prediction_india.csv | 3,000 | rahul-saha18/India-Road-Accident-EDA (GitHub) |
| data/ndap_accident_dataset.csv | 1,350 | NITI Aayog NDAP (Official Government Records) |

All datasets are REAL, verified Indian accident records. NO synthetic data.
