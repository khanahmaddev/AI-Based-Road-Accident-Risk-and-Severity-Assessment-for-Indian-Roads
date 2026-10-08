# Project Progress Tracking

**Project:** AI-Based Road Accident Risk and Severity Assessment for Indian Roads (ALL INDIA)  
**Last Updated:** 2026-10-08 00:37 IST

---

## 1. Completed Steps

### Phase 1: Data Acquisition & ML Model Training ✅
- [x] **Step 1: Dataset Identification & Schema Verification**
  - Queried public Indian road accident datasets on GitHub and verified real public sources.
  - Selected `indian_roads_dataset.csv` (20,000 rows with GPS), `accident_prediction_india.csv` (3,000 rows, 32 States/UTs), and `ndap_accident_dataset.csv` (NITI Aayog official).
- [x] **Step 2: Dataset Acquisition**
  - `scripts/download_datasets.py` downloads and saves all 3 datasets to `data/`.
- [x] **Step 3: ML Model Training & Comparative Evaluation**
  - Stratified 80/20 split. Trained Random Forest (Balanced), Gradient Boosting, XGBoost.
  - Random Forest selected (Macro F1: 0.3260) — only model maintaining coverage across all three severity tiers.
- [x] **Step 4: Model Export & Inference Testing**
  - Saved to `models/severity_model.joblib`, `models/preprocessor.joblib`, `models/model_metadata.json`.
  - `scripts/test_inference.py` validates P(Minor), P(Major), P(Fatal) outputs.
- [x] **Step 5: Documentation**
  - `docs/dataset_and_models.md` written with full dataset schemas and evaluation metrics.

### Phase 2: Backend + Frontend Implementation ✅
- [x] **Step 6: Spatial Accident Index (`backend/spatial_index.py`)**
  - BallTree with Haversine metric over 20,000 GPS accident points.
  - DBSCAN hotspot clustering: 130 verified hotspots computed.
  - Tested: Pune query → 50 accidents within 5km. Remote query → correctly returns "Historical accident data unavailable."
- [x] **Step 7: Transparent 0–100 Risk Engine (`backend/risk_engine.py`)**
  - 5-component weighted scoring: Historical Density (0–30) + ML Severity (0–30) + Weather (0–15) + Road Geometry (0–15) + Temporal (0–10).
  - Real SHAP TreeExplainer on Random Forest for Fatal class feature attribution.
  - Tested: Pune highway at night in rain → Score 84/100 (VERY HIGH). Remote area → Score with "Historical data unavailable" flag.
- [x] **Step 8: Live Weather Integration (`backend/weather_client.py`)**
  - Open-Meteo API client with WMO weather code mapping.
  - Tested: Delhi (24.8°C, clear), Mumbai (28.7°C, clear) — real-time data returned.
- [x] **Step 9: OSRM Routing & Geocoding (`backend/osrm_client.py`)**
  - OSRM real driving routes + Nominatim geocoding + route segmentation with curve detection.
  - Tested: Mumbai→Pune → 147.7 km, 119.5 mins, 15 segments.
- [x] **Step 10: FastAPI Backend (`backend/main.py`)**
  - Endpoints: `/api/health`, `/api/hotspots`, `/api/model-info`, `/api/route`, `/api/simulate-gps`.
  - All 5 endpoints passed automated testing (`scripts/test_api_endpoints.py`).
  - Delhi→Jaipur (297.6 km, 20 segments) correctly marks segments outside GPS coverage as "historical data unavailable."
- [x] **Step 11: End-to-End Pipeline Integration Test (`scripts/test_pipeline.py`)**
  - Geocoding → OSRM routing → route segmentation → live weather → risk engine → all working together.
- [x] **Step 12: React + TypeScript + TailwindCSS + Leaflet Frontend**
  - `frontend/src/App.tsx`: Main app with route calculation, GPS simulation, model info modal.
  - `frontend/src/components/MapViewer.tsx`: Leaflet map with colored route segments (LOW=green, MEDIUM=yellow, HIGH=orange, VERY HIGH=red), accident markers, hotspot circles, GPS vehicle indicator, interactive legend.
  - `frontend/src/components/InfoPanel.tsx`: Navigation panel with origin/destination inputs, 7 preset Indian corridors, transparent factor breakdown bars, ML probability cards, SHAP explainability, upcoming risk warnings, GPS simulation controls, hotspot details tab.
  - `frontend/src/components/ModelInfoModal.tsx`: Model metrics modal with comparative table and confusion matrix.
  - `frontend/src/types.ts`: Full TypeScript interfaces for all API response types.
  - `frontend/vite.config.ts`: Configured with TailwindCSS v4 plugin and `/api` proxy to backend.
  - **Production build succeeded**: `npm run build` → 0 TypeScript errors, bundle output confirmed.

---

## 2. Current Step (PAUSED — Quota Limit Reached)
- **Step 13: Browser Visual Verification & End-to-End Testing**
  - Both servers were started and running:
    - Backend: `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`
    - Frontend: `npm run dev` at `http://127.0.0.1:5173/`
  - The browser page `http://127.0.0.1:5173/` was loaded (page title confirmed: "AI Road Accident Risk & Severity Assessment | Indian Corridors").
  - **Visual verification was interrupted by quota limit before screenshots could be captured.**
  - The app needs: preset corridor testing, GPS simulation testing, visual polish if needed.

---

## 3. Files Created / Modified

| File | Purpose | Size |
| :--- | :--- | :--- |
| `PROJECT_STATUS.md` | Root project status for session resumption | — |
| `CHANGELOG.md` | Chronological milestone log | — |
| `docs/progress.md` | This file — comprehensive progress tracker | — |
| `docs/dataset_and_models.md` | Dataset schemas & model evaluation metrics | — |
| `data/indian_roads_dataset.csv` | 20,000 real Indian accident records with GPS | 2.7 MB |
| `data/accident_prediction_india.csv` | 3,000 records across 32 Indian States/UTs | 422 KB |
| `data/ndap_accident_dataset.csv` | 1,350 official NITI Aayog NDAP records | 119 KB |
| `models/severity_model.joblib` | Trained Random Forest Classifier (balanced) | — |
| `models/preprocessor.joblib` | Scikit-learn ColumnTransformer pipeline | — |
| `models/model_metadata.json` | Model schema, label mapping, evaluation metrics | — |
| `backend/__init__.py` | Backend package init | — |
| `backend/spatial_index.py` | BallTree spatial index + DBSCAN hotspots | 7.5 KB |
| `backend/risk_engine.py` | 0–100 risk scorer + SHAP explainability | 11.4 KB |
| `backend/weather_client.py` | Open-Meteo live weather client | 3.3 KB |
| `backend/osrm_client.py` | OSRM routing + Nominatim geocoding + segmentation | 7.4 KB |
| `backend/main.py` | FastAPI application with 5 endpoints | 12.3 KB |
| `frontend/index.html` | HTML entry with SEO title and Google Fonts | — |
| `frontend/vite.config.ts` | Vite config with TailwindCSS v4 + API proxy | — |
| `frontend/src/index.css` | TailwindCSS + Leaflet styles + animations | — |
| `frontend/src/types.ts` | TypeScript interfaces for all API types | — |
| `frontend/src/App.tsx` | Main React app component | — |
| `frontend/src/components/MapViewer.tsx` | Leaflet map with route segments and markers | 12.2 KB |
| `frontend/src/components/InfoPanel.tsx` | Navigation information panel | 27.8 KB |
| `frontend/src/components/ModelInfoModal.tsx` | Model verification metrics modal | 7.7 KB |
| `scripts/download_datasets.py` | Automated dataset downloader | — |
| `scripts/train_severity_models.py` | ML training pipeline | — |
| `scripts/test_inference.py` | Model probability verification | — |
| `scripts/test_pipeline.py` | End-to-end integration test | — |
| `scripts/test_api_endpoints.py` | FastAPI endpoint automated tests | — |

---

## 4. Dataset Sources

1. **`indian_roads_dataset.csv`**: [Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025](https://github.com/Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025-Python---Jupyternotebook) — 20,000 rows, GPS, 7 states, 8 cities.
2. **`accident_prediction_india.csv`**: [rahul-saha18/India-Road-Accident-Exploratory-Data-Analysis](https://github.com/rahul-saha18/India-Road-Accident-Exploratory-Data-Analysis.) — 3,000 rows, 32 States/UTs.
3. **`ndap_accident_dataset.csv`**: [NITI Aayog NDAP via Saurabh-Vidyarthi](https://github.com/Saurabh-Vidyarthi/Classification_of_Indian_cities_based_on_road_accident_using_NDAP_Dataset) — 1,350 official records.

---

## 5. Model Evaluation Metrics (4,000 Holdout Test Records)

| Model | Accuracy | Macro F1 | Status |
| :--- | :---: | :---: | :--- |
| **Random Forest (Balanced)** | 39.27% | **0.3260** | **Active (Production)** |
| Gradient Boosting | 53.83% | 0.2543 | Majority-biased |
| XGBoost | 54.05% | 0.2531 | Majority-biased |

---

## 6. Known Problems & Limitations

1. **GPS Coverage**: The 20,000-record dataset covers 7 Indian states (MH, PB, TN, DL, KA, TS, WB). Segments outside these zones correctly show "Historical accident data unavailable" and are scored from weather + geometry only. The project does NOT claim nationwide historical GPS coverage.
2. **Class Imbalance**: 55% Minor / 30% Major / 15% Fatal. Balanced RF selected to maintain fatal detection sensitivity.
3. **Browser verification incomplete**: The frontend loaded in browser but visual testing was interrupted by quota. Needs verification of all preset corridors and GPS simulation.

---

## 7. Exact Next Step to Continue

**Resume from Step 13:**
1. Start backend: `python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000` (from `c:\major project`)
2. Start frontend: `npm run dev` (from `c:\major project\frontend`)
3. Open `http://127.0.0.1:5173/` in browser
4. Verify: Mumbai→Pune auto-loads, colored segments visible, risk panel populated
5. Test all 7 preset corridors (Delhi→Jaipur, Bengaluru→Chennai, etc.)
6. Test GPS simulation ("Drive Route" button) and verify upcoming warning banners
7. Test "Metrics" modal opens with benchmark table
8. Polish any visual issues
9. Update tracking files after Phase 3 completion
