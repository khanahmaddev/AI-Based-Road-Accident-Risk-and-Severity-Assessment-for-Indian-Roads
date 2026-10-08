# Changelog

All notable changes and milestones for the **AI-Based Road Accident Risk and Severity Assessment for Indian Roads** project are documented here.

---

## [2026-10-08] - Milestone 2: Full Backend + Frontend Built & Compiled

### Added
- **Spatial Accident Index (`backend/spatial_index.py`)**:
  - BallTree with Haversine metric over 20,000 real GPS accident points.
  - DBSCAN hotspot clustering: 130 verified accident hotspots computed across India.
  - Radius query with explicit "Historical accident data unavailable" for areas outside coverage.
- **Transparent 0–100 Risk Engine (`backend/risk_engine.py`)**:
  - 5-component weighted scoring: Historical Density (0–30) + ML Severity (0–30) + Weather (0–15) + Road Geometry (0–15) + Temporal (0–10).
  - Real SHAP TreeExplainer for Fatal class feature attribution (not fabricated).
  - Tested across high-risk (Score 84, VERY HIGH) and remote (properly flagged) scenarios.
- **Live Weather Integration (`backend/weather_client.py`)**:
  - Open-Meteo real-time API with WMO weather code mapping and coordinate-level caching.
  - Successfully tested with Delhi and Mumbai live weather data.
- **OSRM Routing & Geocoding (`backend/osrm_client.py`)**:
  - Real OSRM driving routes, Nominatim geocoding, route segmentation with curve detection.
  - Mumbai→Pune: 147.7 km, 119.5 mins, 15 segments verified.
- **FastAPI Backend (`backend/main.py`)**:
  - 5 API endpoints: `/api/health`, `/api/hotspots`, `/api/model-info`, `/api/route`, `/api/simulate-gps`.
  - All endpoints passed automated testing (`scripts/test_api_endpoints.py`).
  - Delhi→Jaipur correctly marks remote segments as "historical data unavailable."
- **React + Leaflet Frontend (`frontend/`)**:
  - Interactive Leaflet map with 4-color route segments (LOW green / MEDIUM yellow / HIGH orange / VERY HIGH red).
  - Real accident marker pins with severity-colored popups (click for date, road type, cause, casualties, coordinates).
  - Hotspot circles with dashed red boundaries and detailed popups.
  - Navigation information panel with origin/destination inputs, 7 preset Indian corridors, travel time selector.
  - Transparent risk factor breakdown bars per segment.
  - ML probability cards: P(Minor), P(Major), P(Fatal).
  - Real SHAP feature impact explainability cards.
  - GPS simulation engine with vehicle tracking marker and dynamic "⚠ HIGH ACCIDENT RISK AHEAD" warning banners.
  - Model verification metrics modal with comparative benchmark table and confusion matrix.
  - Production build succeeded: `npm run build` → 0 TypeScript errors.

### Status
- Backend and frontend are fully built and compilation-verified.
- Browser visual verification was interrupted by API quota limit.
- Next: Resume at Phase 3 (browser testing and visual polish).

---

## [2026-10-07] - Milestone 1: Data Acquisition, ML Training & Evaluation

### Added
- **Dataset Downloader (`scripts/download_datasets.py`)**:
  - Automatically fetches and validates real Indian road accident datasets from public repositories.
  - Stored in `data/`:
    - `indian_roads_dataset.csv` (20,000 incident rows with exact GPS coordinates across major Indian transport hubs).
    - `accident_prediction_india.csv` (3,000 incident rows across 32 Indian States and UTs).
    - `ndap_accident_dataset.csv` (1,350 official records from NITI Aayog NDAP).
- **Model Training Pipeline (`scripts/train_severity_models.py`)**:
  - Preprocessing pipeline with one-hot encoding for road/weather attributes and standard scaling for numerical features.
  - Comparative training and evaluation of Random Forest (Balanced), Gradient Boosting, and XGBoost on a 4,000-sample stratified test set.
  - Exported best balanced model to `models/severity_model.joblib` and preprocessor to `models/preprocessor.joblib`.
  - Serialized performance metrics to `models/model_metadata.json`.
- **Inference Verification (`scripts/test_inference.py`)**:
  - Validated probability outputs `P(Minor)`, `P(Major)`, `P(Fatal)` across real-world road and weather scenarios.
- **Documentation & Tracking**:
  - Detailed findings in `docs/dataset_and_models.md`.
  - Created root `PROJECT_STATUS.md` and `docs/progress.md` for permanent project resumption.
