import os
import joblib
import numpy as np
import pandas as pd
import shap
from typing import Dict, Any, List
from backend.spatial_index import SpatialAccidentIndex

class RiskEngine:
    _instance = None

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "severity_model.joblib")
        prep_path = os.path.join(base_dir, "models", "preprocessor.joblib")
        
        if not os.path.exists(model_path) or not os.path.exists(prep_path):
            raise FileNotFoundError("Trained models not found. Run scripts/train_severity_models.py first.")
            
        print(f"Loading trained severity model from {model_path}...")
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(prep_path)
        self.spatial_index = SpatialAccidentIndex.get_instance()
        
        # Initialize SHAP TreeExplainer on Random Forest model
        print("Initializing SHAP TreeExplainer...")
        self.explainer = shap.TreeExplainer(self.model)
        self.feature_names = list(self.preprocessor.get_feature_names_out())
        print(f"Risk Engine initialized with {len(self.feature_names)} features.")

    def assess_segment(
        self,
        lat: float,
        lon: float,
        weather: Dict[str, Any] = None,
        road_infra: Dict[str, Any] = None,
        temporal: Dict[str, Any] = None,
        radius_meters: float = 1500.0
    ) -> Dict[str, Any]:
        """
        Assess risk for a single route point / segment.
        Returns transparent 0-100 risk score, category, breakdown, SHAP explanation, and real accident markers.
        """
        if weather is None:
            weather = {}
        if road_infra is None:
            road_infra = {}
        if temporal is None:
            temporal = {}

        # 1. Query verified spatial accident index
        spatial_res = self.spatial_index.query_radius(lat, lon, radius_meters=radius_meters)
        has_history = spatial_res["historical_data_available"]
        nearby_accidents = spatial_res["accidents"]
        accident_count = spatial_res["count"]

        # Calculate historical density component (0 - 30 points)
        density_points = 0
        density_detail = ""
        fatal_count = sum(1 for a in nearby_accidents if a["severity"].lower() == "fatal")
        major_count = sum(1 for a in nearby_accidents if a["severity"].lower() == "major")

        if not has_history:
            density_points = 0
            density_detail = "Historical accident data unavailable for this area"
        else:
            # Scaled score: fatal accidents weighted heavier
            raw_density = (fatal_count * 5.0) + (major_count * 2.5) + ((accident_count - fatal_count - major_count) * 1.0)
            density_points = min(30, int(round(raw_density)))
            density_detail = f"{accident_count} verified historical accidents ({fatal_count} fatal, {major_count} major) within {int(radius_meters)}m"

        # 2. Extract ML features
        road_type = road_infra.get("road_type", "highway")
        w_condition = weather.get("condition", "clear").lower()
        w_visibility = weather.get("visibility_category", "high").lower()
        traffic_density = road_infra.get("traffic_density", "medium").lower()
        has_signal = "1" if road_infra.get("traffic_signal", False) else "0"
        is_weekend = "1" if temporal.get("is_weekend", False) else "0"
        is_peak = "1" if temporal.get("is_peak_hour", False) else "0"
        hour = int(temporal.get("hour", 12))
        lanes = int(road_infra.get("lanes", 4))
        temp_c = float(weather.get("temperature_c", 25.0))
        vehicles_involved = int(road_infra.get("vehicles_involved", 2))

        input_df = pd.DataFrame([{
            'road_type': road_type,
            'weather': w_condition,
            'visibility': w_visibility,
            'traffic_density': traffic_density,
            'traffic_signal': has_signal,
            'is_weekend': is_weekend,
            'is_peak_hour': is_peak,
            'hour': hour,
            'lanes': lanes,
            'temperature': temp_c,
            'vehicles_involved': vehicles_involved
        }])

        # Run preprocessing and ML inference
        X_proc = self.preprocessor.transform(input_df)
        probs = self.model.predict_proba(X_proc)[0] # [P(minor), P(major), P(fatal)]
        p_minor, p_major, p_fatal = float(probs[0]), float(probs[1]), float(probs[2])

        # Severity probability component (0 - 30 points)
        # Severity weighting: fatal contributes highest risk
        sev_weight = (0.20 * p_minor) + (0.55 * p_major) + (1.00 * p_fatal)
        severity_points = min(30, int(round(sev_weight * 30)))

        # 3. Weather risk component (0 - 15 points)
        weather_points = 0
        weather_reasons = []
        precipitation = float(weather.get("precipitation_mm", 0.0))
        wind_speed = float(weather.get("wind_speed_kmh", 0.0))
        is_rain = "rain" in w_condition or precipitation > 1.0
        is_fog = "fog" in w_condition or w_visibility == "low"

        if is_rain:
            weather_points += 7
            weather_reasons.append("Rain / wet asphalt")
        if is_fog:
            weather_points += 5
            weather_reasons.append("Low visibility / fog")
        if wind_speed > 35.0:
            weather_points += 3
            weather_reasons.append(f"High wind gust ({wind_speed} km/h)")
        if not weather_reasons:
            weather_reasons.append("Clear environmental conditions")
        weather_points = min(15, weather_points)

        # 4. Road infrastructure geometry component (0 - 15 points)
        road_points = 0
        road_reasons = []
        is_junction = bool(road_infra.get("is_junction", False))
        is_bridge = bool(road_infra.get("is_bridge", False))
        is_curve = bool(road_infra.get("is_curve", False))

        if is_junction:
            road_points += 6
            road_reasons.append("Intersection / junction conflict zone")
        if is_curve:
            road_points += 5
            road_reasons.append("Sharp curve geometry")
        if is_bridge:
            road_points += 4
            road_reasons.append("Bridge / elevated structure")
        if road_type == "highway":
            road_points += 3
            road_reasons.append("High-speed national/state highway corridor")
        if not road_reasons:
            road_reasons.append("Standard road section")
        road_points = min(15, road_points)

        # 5. Time and temporal factor (0 - 10 points)
        time_points = 0
        time_reasons = []
        if hour >= 22 or hour <= 4:
            time_points += 6
            time_reasons.append("Late night / reduced alertness window")
        elif is_peak == "1":
            time_points += 4
            time_reasons.append("Peak rush hour traffic volume")
        if is_weekend == "1":
            time_points += 2
            time_reasons.append("Weekend inter-city travel density")
        if not time_reasons:
            time_reasons.append("Standard daytime traffic window")
        time_points = min(10, time_points)

        # 6. Total Risk Score Calculation (0 - 100)
        total_risk = min(100, max(5, density_points + severity_points + weather_points + road_points + time_points))

        # Risk Tier categorization
        if total_risk <= 30:
            risk_tier = "LOW"
            color = "#22c55e" # Green
        elif total_risk <= 55:
            risk_tier = "MEDIUM"
            color = "#eab308" # Yellow
        elif total_risk <= 75:
            risk_tier = "HIGH"
            color = "#f97316" # Orange
        else:
            risk_tier = "VERY HIGH"
            color = "#ef4444" # Red

        # 7. Compute REAL SHAP values for the severity model
        shap_vals = self.explainer.shap_values(X_proc) # Shape: (1, n_features, 3) or list of 3 arrays
        shap_explanations = []
        try:
            # We focus on Fatal severity class (index 2) SHAP impacts
            if isinstance(shap_vals, list):
                fatal_shap = shap_vals[2][0]
            elif shap_vals.ndim == 3:
                fatal_shap = shap_vals[0, :, 2]
            else:
                fatal_shap = shap_vals[0]

            # Top feature impacts
            top_indices = np.argsort(np.abs(fatal_shap))[::-1][:4]
            for idx in top_indices:
                feat_name = self.feature_names[idx].replace("cat__", "").replace("num__", "")
                impact = float(fatal_shap[idx])
                if abs(impact) > 0.001:
                    shap_explanations.append({
                        "feature": feat_name,
                        "shap_impact": round(impact, 4),
                        "direction": "Increases Fatal Risk" if impact > 0 else "Decreases Fatal Risk"
                    })
        except Exception as e:
            shap_explanations.append({"feature": "model_shap", "shap_impact": 0.0, "note": str(e)})

        # 8. Factor breakdown list
        factor_breakdown = [
            {"factor": "Historical Accident Concentration", "points": density_points, "max_points": 30, "detail": density_detail},
            {"factor": "ML Severity Probability Engine", "points": severity_points, "max_points": 30, "detail": f"P(Fatal)={p_fatal:.1%}, P(Major)={p_major:.1%}, P(Minor)={p_minor:.1%}"},
            {"factor": "Environmental & Weather Conditions", "points": weather_points, "max_points": 15, "detail": ", ".join(weather_reasons)},
            {"factor": "Road Geometry & Infrastructure", "points": road_points, "max_points": 15, "detail": ", ".join(road_reasons)},
            {"factor": "Temporal & Traffic Volume", "points": time_points, "max_points": 10, "detail": ", ".join(time_reasons)}
        ]

        # Active Warnings
        warnings = []
        if fatal_count > 0:
            warnings.append(f"⚠ {fatal_count} fatal accident(s) historically recorded near this segment")
        if is_rain and road_type == "highway":
            warnings.append("⚠ Wet highway conditions: increased braking distance & hydroplaning risk")
        if is_curve and total_risk >= 56:
            warnings.append("⚠ High-risk sharp curve segment")
        if is_junction and traffic_density == "high":
            warnings.append("⚠ High traffic density intersection ahead")

        return {
            "latitude": lat,
            "longitude": lon,
            "risk_score": total_risk,
            "risk_tier": risk_tier,
            "color": color,
            "historical_data_available": has_history,
            "historical_accidents_count": accident_count,
            "fatal_accidents_count": fatal_count,
            "major_accidents_count": major_count,
            "probabilities": {
                "minor": round(p_minor, 4),
                "major": round(p_major, 4),
                "fatal": round(p_fatal, 4)
            },
            "factor_breakdown": factor_breakdown,
            "shap_explanations": shap_explanations,
            "warnings": warnings,
            "nearby_accidents": nearby_accidents[:10] # Top 10 closest for map popups
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RiskEngine()
        return cls._instance
