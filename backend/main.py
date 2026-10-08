import os
import sys
import math
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add workspace root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.spatial_index import SpatialAccidentIndex
from backend.risk_engine import RiskEngine
from backend.osrm_client import OSRMRoutingClient, haversine_km
from backend.weather_client import WeatherClient

app = FastAPI(
    title="India Road Accident Risk & Severity Assessment API",
    description="Explainable 0–100 Route-Segment Risk Assessment for Indian Corridors",
    version="1.0.0"
)

# Enable CORS for frontend UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines at startup
spatial_index = SpatialAccidentIndex.get_instance()
risk_engine = RiskEngine.get_instance()

class RouteRequest(BaseModel):
    start: Optional[str] = None
    destination: Optional[str] = None
    start_lat: Optional[float] = None
    start_lon: Optional[float] = None
    end_lat: Optional[float] = None
    end_lon: Optional[float] = None
    hour: Optional[int] = 14
    is_weekend: Optional[bool] = False
    segment_len_km: Optional[float] = 3.0

class GPSLocationRequest(BaseModel):
    current_lat: float
    current_lon: float
    route_id: Optional[str] = None
    segments: List[Dict[str, Any]]

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "service": "AI-Based Road Accident Risk Assessment (ALL INDIA)",
        "indexed_accidents": len(spatial_index.df) if spatial_index.df is not None else 0,
        "model_loaded": risk_engine.model is not None,
        "version": "1.0.0"
    }

@app.get("/api/hotspots")
def get_hotspots(min_accidents: int = 15):
    """
    Get all pre-computed verified accident hotspots clustered from real Indian accident records.
    """
    hotspots = spatial_index.compute_hotspots(min_samples=min_accidents)
    return {
        "count": len(hotspots),
        "hotspots": hotspots
    }

@app.get("/api/model-info")
def get_model_info():
    """
    Return model architecture, parameters, and actual evaluation metrics.
    """
    import json
    meta_path = os.path.join(BASE_DIR, "models", "model_metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            meta = json.load(f)
        return meta
    return {"status": "Model metadata not found"}

@app.post("/api/route")
def calculate_route_risk(req: RouteRequest):
    """
    Compute real OSRM route, split into segments, assess 0-100 risk for each segment,
    attach live weather and SHAP explainability.
    """
    # 1. Resolve start and end coordinates
    if req.start_lat is not None and req.start_lon is not None:
        start_lat, start_lon = req.start_lat, req.start_lon
        start_name = f"({start_lat:.4f}, {start_lon:.4f})"
    elif req.start:
        start_lat, start_lon, start_name = OSRMRoutingClient.geocode(req.start)
    else:
        raise HTTPException(status_code=400, detail="Start location or coordinates required.")

    if req.end_lat is not None and req.end_lon is not None:
        end_lat, end_lon = req.end_lat, req.end_lon
        end_name = f"({end_lat:.4f}, {end_lon:.4f})"
    elif req.destination:
        end_lat, end_lon, end_name = OSRMRoutingClient.geocode(req.destination)
    else:
        raise HTTPException(status_code=400, detail="Destination location or coordinates required.")

    # 2. Get real OSRM driving route
    try:
        route_data = OSRMRoutingClient.get_route(start_lat, start_lon, end_lat, end_lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Routing service error: {str(e)}")

    # 3. Segment the route
    target_len = max(1.0, min(15.0, float(req.segment_len_km or 3.0)))
    raw_segments = OSRMRoutingClient.segment_route(route_data["coordinates"], target_segment_len_km=target_len)
    
    if not raw_segments:
        raise HTTPException(status_code=400, detail="Unable to segment route.")

    # 4. Assess each segment
    assessed_segments = []
    total_score = 0
    max_score = 0
    total_accidents = 0
    total_fatal = 0
    upcoming_warnings = []

    # Cache weather per route to be snappy
    route_weather_cache = {}

    for i, seg in enumerate(raw_segments):
        mid_lat, mid_lon = seg["mid_coord"]
        
        # Round coordinates for weather caching (~10km)
        w_key = (round(mid_lat, 1), round(mid_lon, 1))
        if w_key not in route_weather_cache:
            route_weather_cache[w_key] = WeatherClient.get_live_weather(mid_lat, mid_lon)
        live_weather = route_weather_cache[w_key]

        # Infer road attributes
        is_highway = (route_data["distance_km"] > 30.0 and i > 0 and i < len(raw_segments) - 1)
        road_type = "highway" if is_highway else "urban"
        
        # Check if any step junction is close to mid-point
        is_junction = False
        for j_lat, j_lon in route_data["junction_coords"][:20]:
            if haversine_km(mid_lat, mid_lon, j_lat, j_lon) < 0.8:
                is_junction = True
                break

        road_infra = {
            "road_type": road_type,
            "is_junction": is_junction,
            "is_curve": seg["is_curve"],
            "lanes": 4 if road_type == "highway" else 2,
            "traffic_density": "high" if is_junction else "medium"
        }

        temporal = {
            "hour": req.hour or 14,
            "is_weekend": req.is_weekend or False,
            "is_peak_hour": (req.hour in [8, 9, 10, 17, 18, 19, 20])
        }

        assessment = risk_engine.assess_segment(
            lat=mid_lat,
            lon=mid_lon,
            weather=live_weather,
            road_infra=road_infra,
            temporal=temporal,
            radius_meters=1500.0
        )

        score = assessment["risk_score"]
        total_score += score
        if score > max_score:
            max_score = score
        total_accidents += assessment["historical_accidents_count"]
        total_fatal += assessment["fatal_accidents_count"]

        # If high risk (>= 56), create upcoming alert candidate
        if score >= 56:
            upcoming_warnings.append({
                "segment_index": i,
                "distance_from_start_km": round(sum(s["distance_km"] for s in raw_segments[:i]), 1),
                "risk_score": score,
                "risk_tier": assessment["risk_tier"],
                "color": assessment["color"],
                "coordinates": [mid_lat, mid_lon],
                "historical_accidents": assessment["historical_accidents_count"],
                "fatal_accidents": assessment["fatal_accidents_count"],
                "reasons": [w for w in assessment["warnings"]] or [f["detail"] for f in assessment["factor_breakdown"] if f["points"] > 5]
            })

        assessed_segments.append({
            "segment_index": i,
            "coordinates": seg["coordinates"], # List of [lat, lon]
            "start_coord": seg["start_coord"],
            "mid_coord": seg["mid_coord"],
            "end_coord": seg["end_coord"],
            "distance_km": seg["distance_km"],
            "risk_score": score,
            "risk_tier": assessment["risk_tier"],
            "color": assessment["color"],
            "historical_data_available": assessment["historical_data_available"],
            "historical_accidents_count": assessment["historical_accidents_count"],
            "fatal_accidents_count": assessment["fatal_accidents_count"],
            "major_accidents_count": assessment["major_accidents_count"],
            "probabilities": assessment["probabilities"],
            "factor_breakdown": assessment["factor_breakdown"],
            "shap_explanations": assessment["shap_explanations"],
            "warnings": assessment["warnings"],
            "weather": live_weather,
            "nearby_accidents": assessment["nearby_accidents"]
        })

    avg_score = round(total_score / len(assessed_segments), 1)
    
    if avg_score <= 30:
        overall_tier = "LOW"
    elif avg_score <= 55:
        overall_tier = "MEDIUM"
    elif avg_score <= 75:
        overall_tier = "HIGH"
    else:
        overall_tier = "VERY HIGH"

    # Identify any real hotspots intersecting the corridor
    all_hotspots = spatial_index.compute_hotspots()
    route_hotspots = []
    for h in all_hotspots:
        # Check distance to any segment mid-point
        for s in assessed_segments:
            d = haversine_km(h["latitude"], h["longitude"], s["mid_coord"][0], s["mid_coord"][1])
            if d <= (h["radius_meters"] / 1000.0 + 2.0):
                route_hotspots.append({**h, "distance_to_route_km": round(d, 2)})
                break

    return {
        "origin": {"name": start_name, "latitude": start_lat, "longitude": start_lon},
        "destination": {"name": end_name, "latitude": end_lat, "longitude": end_lon},
        "summary": {
            "distance_km": route_data["distance_km"],
            "duration_mins": route_data["duration_mins"],
            "average_risk_score": avg_score,
            "max_risk_score": max_score,
            "overall_tier": overall_tier,
            "total_segments": len(assessed_segments),
            "total_historical_accidents_along_route": total_accidents,
            "total_fatal_accidents_along_route": total_fatal,
            "hotspots_count": len(route_hotspots)
        },
        "segments": assessed_segments,
        "hotspots_along_route": route_hotspots[:15],
        "upcoming_warnings": upcoming_warnings
    }

@app.post("/api/simulate-gps")
def simulate_gps_position(req: GPSLocationRequest):
    """
    Given simulated or live browser geolocation (lat, lon), find the active segment
    and generate real-time dynamic 'HIGH ACCIDENT RISK AHEAD' alerts.
    """
    user_lat, user_lon = req.current_lat, req.current_lon
    
    closest_segment = None
    min_dist = float("inf")
    closest_idx = 0
    
    for i, seg in enumerate(req.segments):
        mid = seg["mid_coord"]
        d = haversine_km(user_lat, user_lon, mid[0], mid[1])
        if d < min_dist:
            min_dist = d
            closest_segment = seg
            closest_idx = i

    # Look ahead up to 5 km for high risk
    upcoming_alert = None
    cum_dist_km = 0.0
    for j in range(closest_idx + 1, min(len(req.segments), closest_idx + 6)):
        next_seg = req.segments[j]
        cum_dist_km += next_seg["distance_km"]
        if next_seg["risk_score"] >= 56:
            dist_m = int(cum_dist_km * 1000)
            reasons = []
            if next_seg["fatal_accidents_count"] > 0:
                reasons.append(f"{next_seg['fatal_accidents_count']} fatal accidents nearby")
            if next_seg["historical_accidents_count"] > 0:
                reasons.append(f"{next_seg['historical_accidents_count']} historical accidents")
            if next_seg.get("weather", {}).get("condition") == "rain":
                reasons.append("Rain / slippery asphalt")
            if not reasons:
                reasons.append("Elevated risk corridor")

            upcoming_alert = {
                "active": True,
                "title": "⚠ HIGH ACCIDENT RISK AHEAD",
                "distance_meters": dist_m,
                "target_risk_score": next_seg["risk_score"],
                "target_risk_tier": next_seg["risk_tier"],
                "color": next_seg["color"],
                "reasons": reasons,
                "coordinates": next_seg["mid_coord"]
            }
            break

    return {
        "current_position": [user_lat, user_lon],
        "current_segment_index": closest_idx,
        "current_segment_risk": closest_segment["risk_score"] if closest_segment else 0,
        "current_segment_tier": closest_segment["risk_tier"] if closest_segment else "LOW",
        "distance_to_route_km": round(min_dist, 2),
        "upcoming_alert": upcoming_alert
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
