# Documentation and Diagram Prompts
# AI-Based Road Accident Risk and Severity Assessment for Indian Roads
# Ready-to-use prompts for ChatGPT / Claude / Gemini / any AI tool

---

## HOW TO USE THIS FILE

Copy any prompt below and paste it into ChatGPT, Claude, Gemini, or any AI tool.
Each prompt is specifically written for THIS project — just paste and run.

---

============================================================
SECTION 1: PROJECT DOCUMENTATION PROMPTS
============================================================

---

## PROMPT 1 — Full Project Report / Synopsis (for College Submission)

Copy and paste this prompt:

---
Write a full project report for a college final year project titled:
"AI-Based Road Accident Risk and Severity Assessment for Indian Roads"

Project details:
- Scope: All India — National Coverage (all 28 states and 8 Union Territories)
- Dataset: 24,350 real Indian road accident records from 3 sources:
  1. indian_roads_dataset.csv — 20,000 records with GPS coordinates, 7 Indian states, 8 cities
  2. accident_prediction_india.csv — 3,000 records across 32 Indian States/UTs
  3. ndap_accident_dataset.csv — 1,350 official NITI Aayog NDAP government records
- ML Model: Balanced Random Forest Classifier (Macro F1: 0.3260, Accuracy: 39.27%)
  - Compared with: Gradient Boosting (Macro F1: 0.2543) and XGBoost (Macro F1: 0.2531)
  - Selected because it fairly detects all 3 severity classes: Minor, Major, Fatal
- SHAP Explainability: Real SHAP TreeExplainer for Fatal class feature attribution
- Risk Score: Transparent 0-100 score from 5 weighted factors:
  1. Historical Accident Density (max 30 points)
  2. ML Severity Probability (max 30 points)
  3. Live Weather from Open-Meteo API (max 15 points)
  4. Road Geometry / curve detection (max 15 points)
  5. Temporal factor — hour and day (max 10 points)
- Backend: Python FastAPI with 5 API endpoints
- Frontend: React + TypeScript + Vite + Leaflet + OpenStreetMap (no API key)
- Routing: OSRM real road routing with Nominatim geocoding
- Spatial Index: BallTree (Haversine) over 20,000 GPS accident points
- DBSCAN clustering: 130 verified accident hotspots computed
- GPS Simulation: Real-time "Drive Route" mode with upcoming risk warnings
- 7 preset Indian corridors: Mumbai-Pune, Delhi-Jaipur, Bengaluru-Chennai, Chennai-Hyderabad, Kolhapur-Bengaluru, Kolkata-Bhubaneswar, Delhi-Mumbai

Write a formal project report with these sections:
1. Abstract (200 words)
2. Introduction
3. Problem Statement
4. Objectives
5. Literature Review (5 references in IEEE format)
6. Methodology
7. System Architecture
8. Dataset Description
9. ML Model Comparison and Selection
10. Results and Evaluation
11. System Features
12. Limitations
13. Future Scope
14. Conclusion
15. References

Use formal academic language. The report should be suitable for a BE/BTech Computer Science final year project.
---

---

## PROMPT 2 — Abstract Only (150-200 words)

---
Write a 200-word abstract for a final year engineering project titled:
"AI-Based Road Accident Risk and Severity Assessment for Indian Roads"

Key facts:
- Uses 24,350 real Indian accident records (GPS-tagged, NITI Aayog NDAP + GitHub datasets)
- Balanced Random Forest Classifier (Macro F1: 0.3260) trained to predict Minor/Major/Fatal severity
- SHAP Explainability used for transparent feature attribution
- 0-100 transparent risk score from 5 factors: historical density, ML severity, live weather, road geometry, temporal
- FastAPI backend + React/Leaflet frontend with OpenStreetMap
- OSRM real-road routing, 130 DBSCAN accident hotspots, GPS simulation
- All India coverage — not restricted to one state

Write a concise, technical abstract suitable for college submission. Include: problem, methodology, key results, and conclusion.
---

---

## PROMPT 3 — PPT / Presentation Slide Content

---
Create slide-by-slide content for a 15-slide PowerPoint presentation for this project:
"AI-Based Road Accident Risk and Severity Assessment for Indian Roads"

For each slide, give:
- Slide title
- 4-5 bullet points (short, clear)
- Suggested visual/image description

Project details:
- India has the world's highest road accident fatalities (~180,000 per year as of 2022)
- System uses 24,350 real Indian GPS-tagged accident records
- 3 models compared: Balanced Random Forest (selected, Macro F1: 0.3260), Gradient Boosting (Macro F1: 0.2543), XGBoost (Macro F1: 0.2531)
- SHAP Explainability for transparent AI decisions
- 5-factor 0-100 risk score: historical density, ML severity, live weather (Open-Meteo), road geometry, temporal
- FastAPI + React + Leaflet map
- 7 preset Indian corridors, GPS simulation, real-time risk warnings
- 130 DBSCAN accident hotspots on real OpenStreetMap

Slides needed:
1. Title Slide
2. Problem Statement
3. Indian Road Accident Statistics
4. Objectives
5. System Overview / Architecture
6. Dataset Description
7. ML Model Comparison
8. SHAP Explainability
9. Risk Score Formula
10. Live Map Demo Screenshot Description
11. GPS Simulation Feature
12. API Architecture
13. Results and Testing
14. Limitations and Future Scope
15. Conclusion

Make slide content concise, impactful, and suitable for a 10-minute college presentation.
---

---

## PROMPT 4 — Research Paper (IEEE Format)

---
Write a short research paper (3000-4000 words) in IEEE conference paper format for:
"AI-Based Road Accident Risk and Severity Assessment with Explainable Route Risk Mapping for Indian Roads"

Paper structure:
- Abstract (150 words)
- I. Introduction
- II. Related Work (cite 6-8 relevant papers on accident severity prediction, ML road safety, India road accidents)
- III. Dataset and Preprocessing
- IV. Proposed Methodology
- V. Experimental Results
- VI. System Implementation
- VII. Conclusion and Future Work
- References (IEEE format)

Technical specifications:
- Dataset: 24,350 real Indian accident records (NDAP + Prashantsundar + Rahul-Saha GitHub datasets)
- Models: Random Forest (Balanced), Gradient Boosting, XGBoost — comparative study
- Selected model: Random Forest with Macro F1 = 0.3260, Accuracy = 39.27%
- SHAP TreeExplainer for explainability
- 5-factor risk score (0-100): historical density (30), ML severity (30), weather (15), geometry (15), temporal (10)
- BallTree spatial indexing with Haversine metric over 20,000 GPS points
- DBSCAN for accident hotspot clustering (130 hotspots, eps=0.05°, min_samples=5)
- FastAPI REST backend, React+Leaflet frontend, OpenStreetMap tiles

Use formal IEEE writing style. All statements must be technically accurate based on the project.
---

---

## PROMPT 5 — Viva Questions and Answers

---
Generate 30 likely viva/oral exam questions and detailed answers for a final year project:
"AI-Based Road Accident Risk and Severity Assessment for Indian Roads"

Project technical stack:
- Python: FastAPI, scikit-learn, imbalanced-learn, SHAP, scipy, pandas, numpy
- Frontend: React, TypeScript, Vite, Leaflet, OpenStreetMap, TailwindCSS
- ML: Random Forest (Balanced), Gradient Boosting, XGBoost
- Spatial: BallTree (Haversine), DBSCAN clustering
- APIs: OSRM routing, Nominatim geocoding, Open-Meteo weather
- Dataset: 24,350 real Indian accident records with GPS coordinates

Include questions on:
1. Why Random Forest over XGBoost despite lower raw accuracy?
2. What is Macro F1 and why is it better than accuracy for imbalanced data?
3. How does SHAP explainability work in this system?
4. How is the 0-100 risk score calculated?
5. What is BallTree and why is it used?
6. What is DBSCAN and how were hotspots identified?
7. Why OpenStreetMap over Google Maps?
8. How does OSRM routing work?
9. How does GPS simulation work?
10. What is class imbalance and how was it handled?

Provide detailed technical answers for each question.
---

---

## PROMPT 6 — README.md for GitHub

---
Write a professional GitHub README.md for this project:

Project Name: AI-Based Road Accident Risk and Severity Assessment for Indian Roads

Include:
- Project badge row (Python, React, FastAPI, License MIT)
- One-line description
- Demo screenshot placeholder section
- Features list
- Tech stack table
- Quick start (3-step setup)
- API endpoint table
- Dataset sources
- Model accuracy comparison table
- Project structure tree
- Contributing section
- License section

Technical facts:
- Python FastAPI backend, React+TypeScript+Vite frontend
- OpenStreetMap (Leaflet) — no paid API key needed
- 24,350 real Indian accident records
- Random Forest (Balanced) — Macro F1: 0.3260
- SHAP explainability
- 5-factor 0-100 risk score
- OSRM real routing
- 130 DBSCAN hotspots
- GPS simulation / Drive Route mode
- 7 preset Indian corridors
- All India coverage

Write in standard GitHub README markdown format with emoji headers.
---

---

============================================================
SECTION 2: DIAGRAM PROMPTS
============================================================

---

## DIAGRAM PROMPT 1 — System Architecture Diagram (for Mermaid / Draw.io)

---
Generate a Mermaid.js system architecture diagram for this project.

The system has:

User Layer:
- Web Browser (React + Leaflet)
- Input: Origin city, Destination city, Hour, Weekend flag

Frontend Components:
- MapViewer.tsx (OpenStreetMap + route rendering)
- InfoPanel.tsx (dashboard, preset corridors, GPS controls)
- ModelInfoModal.tsx (ML metrics display)

API Layer (FastAPI - port 8000):
- GET /api/health
- GET /api/hotspots
- GET /api/model-info
- POST /api/route
- POST /api/simulate-gps

Backend Modules:
- osrm_client.py → OSRM API (router.project-osrm.org) + Nominatim geocoding
- spatial_index.py → BallTree (Haversine) spatial index over 20,000 GPS accident points
- risk_engine.py → 5-factor 0-100 risk scorer + SHAP TreeExplainer
- weather_client.py → Open-Meteo API (live weather)

Data Layer:
- indian_roads_dataset.csv (20,000 records)
- accident_prediction_india.csv (3,000 records)
- ndap_accident_dataset.csv (1,350 records)
- severity_model.joblib (trained Random Forest)
- preprocessor.joblib (ColumnTransformer)

External APIs:
- OSRM (router.project-osrm.org) — real road routing
- Nominatim (nominatim.openstreetmap.org) — geocoding
- Open-Meteo (api.open-meteo.com) — live weather

Generate a clear Mermaid.js flowchart or architecture diagram showing data flow from user input to risk score output.
---

---

## DIAGRAM PROMPT 2 — ML Pipeline Flowchart

---
Create a Mermaid.js flowchart showing the complete ML training and inference pipeline for this accident severity prediction system.

Training Pipeline:
1. Load 3 CSV datasets (24,350 total records)
2. Merge and deduplicate
3. Label encode severity (Minor=0, Major=1, Fatal=2)
4. Feature selection: road_type, weather, hour, junction, cause, casualties
5. Train-test split (80% train, 20% test, stratified)
6. ColumnTransformer: OneHotEncoder for categorical + StandardScaler for numerical
7. Train 3 models: Random Forest (Balanced), Gradient Boosting, XGBoost
8. Evaluate each: Accuracy + Macro F1 + Confusion Matrix
9. Select best by Macro F1: Random Forest (F1=0.3260)
10. Save: severity_model.joblib + preprocessor.joblib + model_metadata.json

Inference Pipeline (at prediction time):
1. Receive route segment mid-coordinates
2. Query BallTree → get 50 nearest accidents within 5km
3. Calculate historical density score (0-30 pts)
4. Extract road_type, weather, hour from request
5. Transform features with preprocessor.joblib
6. Predict: P(Minor), P(Major), P(Fatal) with severity_model.joblib
7. Calculate ML severity score from P(Fatal) (0-30 pts)
8. Call Open-Meteo API → weather score (0-15 pts)
9. Detect road curves from GPS polyline → geometry score (0-15 pts)
10. Calculate temporal score from hour + weekend (0-10 pts)
11. Sum all factors → Total Risk Score (0-100)
12. Classify: LOW / MEDIUM / HIGH / VERY HIGH
13. Run SHAP TreeExplainer → top feature attributions
14. Return full JSON response to frontend

Draw this as a clear flowchart with decision nodes and data stores.
---

---

## DIAGRAM PROMPT 3 — Risk Score Calculation Formula Diagram

---
Create a visual diagram (using Mermaid or ASCII art) showing the 5-factor risk score formula for this road accident risk system.

Risk Score (0-100) = Sum of 5 components:

Component 1 — Historical Accident Density (max 30 points):
- Query 20,000 GPS accident points within 5km radius of segment midpoint
- Score = min(accident_count / 3, 30)
- Source: BallTree spatial index over indian_roads_dataset.csv

Component 2 — ML Severity Score (max 30 points):
- Input: road_type, weather, hour, junction, cause
- Model: Balanced Random Forest trained on 24,350 Indian records
- P(Fatal) and P(Major) used to compute score
- Score = (P_fatal * 30) + (P_major * 15)
- Source: severity_model.joblib

Component 3 — Weather Risk (max 15 points):
- Live weather from Open-Meteo API at segment GPS coordinates
- Rain/storm: +15, Fog: +12, Drizzle: +8, Clear night: +5, Clear day: +0
- Also adds points for wind > 50 km/h and low visibility

Component 4 — Road Geometry (max 15 points):
- Detect curve from GPS polyline angle variance (>35 degrees)
- Detect ghat/mountain section from altitude change
- Sharp curve: +15, Mild curve: +7, Straight: +0

Component 5 — Temporal Risk (max 10 points):
- Night hours (20:00 to 05:00): +10
- Evening peak (17:00 to 20:00): +6
- Weekend: +3 additional
- Day time: +0

Final Classification:
- 0-30: LOW (Green)
- 31-55: MEDIUM (Yellow/Amber)
- 56-75: HIGH (Orange)
- 76-100: VERY HIGH (Red)

Show this as a visual formula breakdown diagram.
---

---

## DIAGRAM PROMPT 4 — Entity Relationship / Data Flow Diagram

---
Draw an Entity Relationship (ER) or Data Flow Diagram (DFD) for this road accident risk system.

Entities and their attributes:

AccidentRecord:
- accident_id (PK)
- latitude, longitude
- severity (Minor/Major/Fatal)
- road_type, junction_type
- weather_condition, time_of_day
- cause, casualties
- city, state, date

RouteSegment:
- segment_index (PK)
- start_coord, end_coord, mid_coord
- distance_km
- risk_score (0-100)
- risk_tier (LOW/MEDIUM/HIGH/VERY HIGH)
- historical_data_available (boolean)
- historical_accidents_count
- fatal_accidents_count

RiskScore:
- historical_density_pts (0-30)
- ml_severity_pts (0-30)
- weather_pts (0-15)
- geometry_pts (0-15)
- temporal_pts (0-10)
- total (0-100)

SHAPExplanation:
- feature_name
- shap_value
- direction (increases/decreases risk)

Hotspot (DBSCAN cluster):
- cluster_id (PK)
- latitude, longitude, radius_meters
- total_accidents, fatal_count, major_count
- risk_score, top_causes
- cities, states

WeatherData:
- latitude, longitude
- temperature_c, wind_speed_kmh
- precipitation_mm, weather_code, condition

Route:
- origin_name, origin_lat, origin_lon
- destination_name, destination_lat, destination_lon
- distance_km, duration_mins
- segments (list of RouteSegment)
- hotspots_along_route (list of Hotspot)

Show relationships between all entities.
---

---

## DIAGRAM PROMPT 5 — DBSCAN Hotspot Clustering Diagram

---
Explain and draw a diagram showing how DBSCAN clustering was used to identify accident hotspots in this project.

DBSCAN parameters used:
- eps = 0.05 degrees (approximately 5km radius)
- min_samples = 5 (minimum 5 accidents to form a cluster)
- metric = haversine
- Input: 20,000 GPS accident point coordinates (latitude, longitude)
- Output: 130 verified accident hotspot clusters

For each cluster (hotspot):
- Center coordinates (centroid of all points in cluster)
- Radius in meters
- Total accidents, fatal count, major count
- Top causes of accidents in cluster
- Risk score for the hotspot
- City and state labels

Create a diagram showing:
1. Raw scatter plot of 20,000 accident GPS points across India
2. DBSCAN grouping nearby points into clusters
3. Noise points (not part of any cluster)
4. Final 130 hotspot circles on map
5. Example: Mumbai highway hotspot with 47 accidents, 8 fatal, radius 4.2km

Explain each step clearly as a flowchart.
---

---

## DIAGRAM PROMPT 6 — Frontend Component Tree

---
Draw a React component tree diagram for this web application frontend.

App.tsx (root):
State:
- routeData (RouteResponse)
- selectedSegment (RouteSegment)
- allHotspots (Hotspot[])
- isLoading (boolean)
- showAccidents (boolean)
- showHotspots (boolean)
- isSimulating (boolean)
- simulatedGpsPos ([lat, lon])
- activeGpsAlert (alert object)
- isModelInfoOpen (boolean)

Children:
1. MapViewer.tsx (left panel, 70% width)
   - Leaflet Map container
   - OpenStreetMap TileLayer (tile.openstreetmap.org)
   - Route Polylines (color-coded by risk)
   - Origin Marker (green pin A)
   - Destination Marker (red pin B)
   - AccidentCircleMarkers (red/orange/yellow dots)
   - HotspotCircles (dashed red areas)
   - GPS Vehicle Marker (pulsing blue dot)
   - Zoom Controls (custom, top-right)
   - Fit Route Button
   - Risk Legend (bottom-left)

2. InfoPanel.tsx (right panel, 30% width)
   - Header (logo + Metrics button)
   - Route Planner Form (origin input, destination input, hour select, weekend checkbox)
   - Preset Corridors (7 buttons)
   - GPS Alert Banner (conditional)
   - Map Overlays Toggle (Accident Pins, Hotspots)
   - GPS Simulation Controls (Drive Route, Pause, Reset)
   - Tab Navigation (Corridor Overview, Segment Details, Hotspots)
   - Overview Tab: Stats Grid, Data Notice, Segments List
   - Segment Tab: Risk breakdown bars, ML probabilities, SHAP cards
   - Hotspots Tab: Cluster cards

3. ModelInfoModal.tsx (modal overlay)
   - Dataset statistics
   - ML benchmark comparison table
   - Confusion matrix display

Draw this as a tree diagram with props flowing downward.
---

---

## DIAGRAM PROMPT 7 — Sequence Diagram (User Request to Risk Score)

---
Create a UML sequence diagram showing the complete flow when a user clicks "Assess Route Risk" in this web application.

Participants:
- User (browser)
- React Frontend (App.tsx)
- FastAPI Backend (main.py)
- OSRMClient (osrm_client.py)
- OSRM API (router.project-osrm.org)
- Nominatim API (nominatim.openstreetmap.org)
- SpatialIndex (spatial_index.py)
- RiskEngine (risk_engine.py)
- WeatherClient (weather_client.py)
- Open-Meteo API (api.open-meteo.com)
- ML Model (severity_model.joblib)

Sequence:
1. User types "Mumbai" and "Pune" and clicks "Assess Route Risk"
2. Frontend sends POST /api/route with JSON payload
3. FastAPI receives request, calls OSRMClient.geocode("Mumbai")
4. OSRMClient calls Nominatim API → returns (19.0760, 72.8777)
5. OSRMClient.geocode("Pune") → returns (18.5204, 73.8567)
6. OSRMClient.get_route() calls OSRM API with coordinates
7. OSRM returns 2539-point GeoJSON polyline, 147.7km, 119.5 mins
8. OSRMClient.segment_route() splits into 15 segments of ~10km each
9. For each segment (loop 15 times):
   a. SpatialIndex.query() finds 50 nearest accidents within 5km
   b. WeatherClient.get_weather() calls Open-Meteo API at segment midpoint
   c. RiskEngine.score_segment() runs ML model prediction
   d. ML Model returns P(Minor), P(Major), P(Fatal)
   e. RiskEngine computes 5-factor risk score (0-100)
   f. RiskEngine runs SHAP TreeExplainer for top 3 features
10. FastAPI aggregates all 15 segments into RouteResponse JSON
11. Frontend receives JSON, updates React state
12. MapViewer renders colored polylines, accident markers, hotspots on Leaflet map
13. InfoPanel shows risk statistics, segment list, weather data

Show all API calls, database queries, and response times.
---

---

## DIAGRAM PROMPT 8 — Deployment / Infrastructure Diagram

---
Create a deployment/infrastructure diagram for this project.

Local Development Setup:
- Developer Machine (Windows)
  - Terminal 1: Python Uvicorn → FastAPI (localhost:8000)
  - Terminal 2: Vite Dev Server → React (localhost:5173)
  - Vite proxy: /api/* → localhost:8000

External Services (Free, No API Key):
- router.project-osrm.org → Road routing
- nominatim.openstreetmap.org → Geocoding
- api.open-meteo.com → Weather data
- tile.openstreetmap.org → Map tiles (in browser)

Local Data (on disk):
- data/indian_roads_dataset.csv (20,000 records, 2.7MB)
- data/accident_prediction_india.csv (3,000 records, 422KB)
- data/ndap_accident_dataset.csv (1,350 records, 119KB)
- models/severity_model.joblib
- models/preprocessor.joblib

Production Deployment Options (future):
- Backend: Docker + AWS EC2 / Railway / Render
- Frontend: Vercel / Netlify
- Database: PostgreSQL with PostGIS (for spatial queries at scale)

Draw this as an infrastructure/deployment diagram showing all components and their connections.
---

---

============================================================
SECTION 3: SPECIFIC TOOL PROMPTS
============================================================

---

## DRAW.IO (diagrams.net) Prompt

---
I need to create a system architecture diagram in draw.io for my project.

Please describe exactly what shapes, arrows, and labels to place in draw.io for this architecture:

Project: AI-Based Road Accident Risk Assessment for Indian Roads
Backend: FastAPI (Python) on port 8000
Frontend: React + Leaflet on port 5173
External APIs: OSRM, Nominatim, Open-Meteo, OpenStreetMap tiles
Local data: 3 CSV files + 2 .joblib model files

Describe:
1. What shapes to use for each component
2. What color to give each layer (User/Frontend/Backend/Data/External)
3. What arrows to draw between components
4. What labels to put on each arrow (data flow description)
5. Layout recommendation (top-down or left-right)
---

---

## CANVA / INFOGRAPHIC Prompt

---
Create an infographic design description for this road accident AI project.

Title: "AI Route Risk Assessment — How It Works"

Design a step-by-step infographic with 6 panels:

Panel 1 — Input
Icon: Map pin / car
Text: "User enters Origin + Destination city"
Subtext: "Example: Chennai to Hyderabad"

Panel 2 — Real Road Routing
Icon: Road/highway
Text: "OSRM calculates actual driving route"
Subtext: "627 km, 42 route segments on real roads"

Panel 3 — Historical Data
Icon: Database / accident records
Text: "BallTree queries 20,000 GPS accident points"
Subtext: "Finds all accidents within 5km of route"

Panel 4 — AI Prediction
Icon: Brain / neural network
Text: "Random Forest ML model predicts severity"
Subtext: "P(Minor) + P(Major) + P(Fatal) for each segment"

Panel 5 — Risk Score
Icon: Gauge / speedometer
Text: "0-100 transparent risk score per segment"
Subtext: "5 factors: History + ML + Weather + Geometry + Time"

Panel 6 — Live Map
Icon: Map with colored route
Text: "Color-coded route displayed on OpenStreetMap"
Subtext: "Green = Low, Yellow = Medium, Orange = High, Red = Very High"

Use the color scheme: Deep navy background with emerald green, amber, orange, and red accents.
Include India map silhouette as background element.
---

---

## LUCIDCHART Prompt

---
I need to create a data flow diagram (DFD) in Lucidchart for my final year project.

Project: AI-Based Road Accident Risk and Severity Assessment for Indian Roads

Level 0 DFD (Context Diagram):
- One central process: "Road Accident Risk Assessment System"
- External entities:
  * Driver/User (input: route details, output: risk assessment map)
  * OSRM Server (input: coordinates, output: route geometry)
  * Open-Meteo (input: GPS coordinates, output: weather data)
  * OpenStreetMap (output: map tiles)
  * Indian Accident Database (output: historical records)

Level 1 DFD:
Break the central process into 5 sub-processes:
1. Route Planning (geocoding + OSRM routing)
2. Spatial Accident Lookup (BallTree query)
3. ML Severity Prediction (Random Forest inference)
4. Risk Score Calculation (5-factor weighted sum)
5. Visualization (Leaflet map rendering)

Show data stores:
- D1: Accident Records (CSV files)
- D2: Trained ML Model (joblib files)
- D3: Route Cache (in-memory)

Describe what shapes and arrows to use in Lucidchart, with exact labels.
---

---

Last Updated: 2026-10-08
Total Prompts: 8 Documentation + 8 Diagram + 3 Tool-specific = 19 prompts
