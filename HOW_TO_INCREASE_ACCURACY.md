# How to Increase Project Accuracy
# AI-Based Road Accident Risk and Severity Assessment — Indian Roads

---

## Current Accuracy (Baseline)

| Model | Accuracy | Macro F1 | Status |
|-------|----------|----------|--------|
| Random Forest (Balanced) | 39.27% | 0.3260 | SELECTED (production) |
| Gradient Boosting | 53.83% | 0.2543 | Rejected — biased to Minor class |
| XGBoost | 54.05% | 0.2531 | Rejected — biased to Minor class |

WHY Macro F1 matters more than raw Accuracy:
- 55% of accidents are "Minor" in the dataset
- Gradient Boosting/XGBoost predict "Minor" for almost everything = false high accuracy
- Macro F1 = 0.3260 means Random Forest fairly detects all 3 classes (Minor, Major, Fatal)
- Fatal detection is critical for a road safety system

Realistic Target After All Improvements: Macro F1 --> 0.55 to 0.65
---

## PRIORITY ORDER (Highest Impact First)

| Priority | Method | Effort | Expected Macro F1 Gain |
|----------|--------|--------|-----------------------|
| 1 | SMOTE Oversampling | Low (1-2 hours) | +5 to 8% |
| 2 | Add New Features | Medium (1 day) | +6 to 12% |
| 3 | Optuna Hyperparameter Tuning | Medium (2-3 hours) | +3 to 6% |
| 4 | Ensemble Voting (RF + XGB + LGBM) | Medium (half day) | +4 to 8% |
| 5 | Add Larger Indian Datasets | High (2-3 days) | +10 to 20% |

---

## METHOD 1 — Fix Class Imbalance with SMOTE (Quickest Win)

### Problem:
The dataset has severe imbalance:
- Minor: 55%
- Major: 30%
- Fatal: 15%

### Current approach (basic):
class_weight='balanced' in RandomForestClassifier

### Better approach — SMOTE (Synthetic Minority Oversampling Technique):

Install:
    pip install imbalanced-learn

Code change in scripts/train_severity_models.py:

    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline

    # Apply SMOTE before training
    smote = SMOTE(sampling_strategy='auto', random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_train_transformed, y_train)

    # Train on resampled balanced data
    rf_model = RandomForestClassifier(
        n_estimators=300,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_resampled, y_resampled)

### Alternative — ADASYN (Adaptive Synthetic Sampling):

    from imblearn.over_sampling import ADASYN
    adasyn = ADASYN(sampling_strategy='auto', random_state=42)
    X_resampled, y_resampled = adasyn.fit_resample(X_train, y_train)

Expected improvement: +5 to 8% Macro F1

---

## METHOD 2 — Add More Meaningful Features

### Current features used:
- road_type, weather_condition, hour_of_day, junction_type, cause, casualties

### High-impact features to ADD:

| Feature | Why Important | Where to Get |
|---------|--------------|--------------|
| speed_limit | Directly correlated with Fatal severity | OpenStreetMap / NHAI road data |
| vehicle_type | Trucks vs Cars have very different fatality rates | MoRTH annual report |
| district_code | Location-based historical fatality rate | Census of India |
| month | Monsoon months = 40% more accidents | Already in date column |
| road_surface | Wet/dry/damaged surface condition | PWD / NHAI data |
| visibility_meters | Fog, rain, smoke directly raise Fatal rate | IMD weather data |
| lighting_condition | No streetlight + night = Fatal hotspot | Field survey / iRAD |
| alcohol_involved | Binary flag — high Fatal correlation | Police FIR records |
| road_divider | Undivided highways = head-on Fatal crashes | NHAI road geometry |
| gradient_percent | Steep slopes raise crash severity | SRTM elevation data |

### How to add new feature (example — extract month):

In scripts/train_severity_models.py:

    import pandas as pd

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.month
    df['is_monsoon'] = df['month'].apply(lambda m: 1 if m in [6,7,8,9] else 0)
    df['is_night'] = df['hour'].apply(lambda h: 1 if h >= 20 or h <= 5 else 0)
    df['is_fog_season'] = df['month'].apply(lambda m: 1 if m in [11,12,1,2] else 0)

Expected improvement: +6 to 12% Macro F1

---

## METHOD 3 — Hyperparameter Tuning with Optuna

### Install:
    pip install optuna

### Add to scripts/train_severity_models.py:

    import optuna
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import f1_score

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 25),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 15),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
            'class_weight': 'balanced',
            'random_state': 42,
            'n_jobs': -1
        }
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return f1_score(y_test, y_pred, average='macro')

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100, show_progress_bar=True)

    print("Best Macro F1:", study.best_value)
    print("Best Params:", study.best_params)

    # Train final model with best params
    best_model = RandomForestClassifier(**study.best_params, class_weight='balanced', random_state=42)
    best_model.fit(X_train, y_train)

### Run command:
    python scripts/train_severity_models.py

Expected improvement: +3 to 6% Macro F1

---

## METHOD 4 — Ensemble Voting Classifier (RF + XGBoost + LightGBM)

### Install LightGBM:
    pip install lightgbm

### Code:

    from sklearn.ensemble import VotingClassifier, RandomForestClassifier
    from xgboost import XGBClassifier
    import lightgbm as lgb

    rf = RandomForestClassifier(
        n_estimators=500, class_weight='balanced', random_state=42, n_jobs=-1
    )

    xgb = XGBClassifier(
        n_estimators=500,
        scale_pos_weight=3.5,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        use_label_encoder=False,
        eval_metric='mlogloss',
        random_state=42
    )

    lgbm = lgb.LGBMClassifier(
        n_estimators=500,
        class_weight='balanced',
        learning_rate=0.05,
        num_leaves=63,
        random_state=42
    )

    # Soft voting uses probability averages
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('xgb', xgb), ('lgbm', lgbm)],
        voting='soft'
    )
    ensemble.fit(X_train, y_train)

    # Evaluate
    y_pred = ensemble.predict(X_test)
    print("Ensemble Macro F1:", f1_score(y_test, y_pred, average='macro'))

Expected improvement: +4 to 8% Macro F1

---

## METHOD 5 — Add More Real Indian Accident Data

### Current dataset size: 24,350 records (3 CSV files)

### Where to get more free Indian data:

| Source | URL | Records | Notes |
|--------|-----|---------|-------|
| data.gov.in (MoRTH) | https://data.gov.in | 100,000+ | Official government road accident data |
| iRAD (Integrated Road Accident Database) | https://irad.nic.in | Active | Real-time FIR-linked accident records |
| NDAP (NITI Aayog) | https://ndap.gov.in | 5,000+ | More tables available |
| Kaggle India Road Accidents | https://kaggle.com | 50,000+ | Search: "India road accident dataset" |
| NHAI Black Spot List | https://nhai.gov.in | 789 black spots | Verified high-fatality locations |
| OpenCity.in | https://opencity.in | Various | City-level road accident reports |

### How to merge new dataset:

    import pandas as pd

    df1 = pd.read_csv('data/indian_roads_dataset.csv')
    df_new = pd.read_csv('data/new_morth_data.csv')

    # Standardize column names
    df_new = df_new.rename(columns={
        'Accident_Severity': 'severity',
        'Road_Type': 'road_type',
        'Weather_Conditions': 'weather',
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    })

    # Merge
    df_combined = pd.concat([df1, df_new], ignore_index=True)
    df_combined.drop_duplicates(inplace=True)
    df_combined.to_csv('data/combined_dataset.csv', index=False)

    print(f"Combined dataset: {len(df_combined)} records")

Expected improvement: +10 to 20% Macro F1 (largest single impact)

---

## METHOD 6 — Cross-Validation (More Reliable Evaluation)

Currently using single 80/20 train-test split.
Use 5-fold Stratified Cross-Validation for more reliable accuracy measurement:

    from sklearn.model_selection import StratifiedKFold, cross_validate
    from sklearn.metrics import make_scorer, f1_score

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scorer = make_scorer(f1_score, average='macro')

    results = cross_validate(
        rf_model, X_transformed, y,
        cv=cv,
        scoring=scorer,
        return_train_score=True
    )

    print("CV Macro F1 scores:", results['test_score'])
    print("Mean CV Macro F1:", results['test_score'].mean())
    print("Std:", results['test_score'].std())

This does NOT increase accuracy — it gives you a more honest/reliable accuracy number.

---

## METHOD 7 — Improve Risk Score Beyond ML Model

The 0-100 risk score uses 5 weighted factors.
Each factor can be improved independently:

### Current factor weights:
    Historical Density (0-30 pts)  -- 30% weight
    ML Severity       (0-30 pts)  -- 30% weight
    Weather           (0-15 pts)  -- 15% weight
    Road Geometry     (0-15 pts)  -- 15% weight
    Temporal          (0-10 pts)  -- 10% weight

### How to improve each factor:

1. Historical Density:
   - Add MoRTH 100k+ records (expand from 7 states to all 28+ states)
   - Reduces "Historical data unavailable" segments from ~60% to ~20%

2. ML Severity:
   - Apply Methods 1-5 above
   - Each improvement directly raises the 30-point ML component accuracy

3. Weather:
   - Currently: wind, temperature, precipitation from Open-Meteo
   - Add: fog density from IMD, AQI (dust reduces visibility), cyclone alerts
   - Source: https://api.imdpune.gov.in (free IMD API)

4. Road Geometry:
   - Currently: curve detection from GPS polyline
   - Add: official NHAI road quality index score per highway segment
   - Add: elevation change (steep gradient = higher risk)
   - Source: SRTM elevation data (free), NHAI reports

5. Temporal:
   - Currently: hour + is_weekend
   - Add: is_festival (Diwali, Holi, Eid = historically 3x accident rate)
   - Add: is_school_time (morning rush hour)
   - Add: month (monsoon June-September = +40% accident rate)

---

## SUMMARY — Expected Total Improvement

| Stage | Methods Applied | Expected Macro F1 |
|-------|----------------|-------------------|
| Baseline (current) | RF Balanced | 0.3260 |
| After Method 1 | + SMOTE | 0.38 to 0.40 |
| After Method 2 | + New Features | 0.43 to 0.48 |
| After Method 3 | + Optuna Tuning | 0.46 to 0.52 |
| After Method 4 | + Ensemble | 0.50 to 0.56 |
| After Method 5 | + More Data | 0.58 to 0.68 |

Final realistic target: Macro F1 = 0.60+ (roughly 84% relative improvement from baseline)
In terms of raw accuracy: approximately 55% to 65% accuracy on balanced test set

---

## QUICK IMPLEMENTATION ORDER (Step by Step)

Step 1 (Today — 1 hour):
    pip install imbalanced-learn optuna lightgbm
    # Add SMOTE to train_severity_models.py
    python scripts/train_severity_models.py

Step 2 (Today — 2 hours):
    # Add month, is_monsoon, is_night, is_fog_season features
    # Re-run training pipeline

Step 3 (This week):
    # Run Optuna tuning (100 trials, ~30-60 minutes)
    # Save best parameters

Step 4 (This week):
    # Build ensemble: RF + XGBoost + LightGBM

Step 5 (This month):
    # Download MoRTH / iRAD data from data.gov.in
    # Merge and retrain on 100,000+ records

---

## FILES TO EDIT FOR IMPLEMENTATION

| File | What to Change |
|------|----------------|
| scripts/train_severity_models.py | Add SMOTE, new features, Optuna, Ensemble |
| backend/risk_engine.py | Update factor weights if new factors added |
| backend/spatial_index.py | Re-index after adding larger dataset |
| data/ | Add new downloaded CSV datasets |
| models/ | New model files saved after retraining |
| docs/dataset_and_models.md | Document new accuracy metrics |
| PROJECT_STATUS.md | Update accuracy numbers after retraining |

---

Last Updated: 2026-10-08
