import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

def test_endpoints():
    client = TestClient(app)
    
    print("Testing GET /api/health...")
    r = client.get("/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("Health response:", r.json())
    
    print("\nTesting GET /api/model-info...")
    r = client.get("/api/model-info")
    assert r.status_code == 200
    info = r.json()
    print("Best model:", info.get("best_model"))
    print("Metrics keys:", list(info.get("metrics", {}).keys()))
    
    print("\nTesting GET /api/hotspots...")
    r = client.get("/api/hotspots?min_accidents=15")
    assert r.status_code == 200
    hotspots_data = r.json()
    print(f"Total hotspots: {hotspots_data['count']}")
    if hotspots_data["hotspots"]:
        h = hotspots_data["hotspots"][0]
        print(f"Top Hotspot: {h['cities']} - {h['total_accidents']} accidents, Risk: {h['risk_score']}")

    print("\nTesting POST /api/route (Mumbai -> Pune)...")
    r = client.post("/api/route", json={
        "start": "Mumbai",
        "destination": "Pune",
        "hour": 21,
        "is_weekend": True,
        "segment_len_km": 10.0
    })
    assert r.status_code == 200, f"Route calculation failed: {r.text}"
    res = r.json()
    summary = res["summary"]
    print(f"Route Calculated: {summary['distance_km']} km, {summary['duration_mins']} mins")
    print(f"Avg Risk: {summary['average_risk_score']} ({summary['overall_tier']}), Max Risk: {summary['max_risk_score']}")
    print(f"Total Segments: {summary['total_segments']}, Accidents along route: {summary['total_historical_accidents_along_route']}")
    print(f"Upcoming warnings count: {len(res['upcoming_warnings'])}")

    print("\nTesting POST /api/route for remote corridor (Delhi -> Jaipur)...")
    r2 = client.post("/api/route", json={
        "start": "Delhi",
        "destination": "Jaipur",
        "hour": 15,
        "is_weekend": False,
        "segment_len_km": 20.0
    })
    assert r2.status_code == 200
    res2 = r2.json()
    print(f"Delhi -> Jaipur: {res2['summary']['distance_km']} km, Segments: {len(res2['segments'])}")
    # Check if remote segment has clear 'historical_data_available' flag
    has_unavailable = any(not s["historical_data_available"] for s in res2["segments"])
    print(f"Includes segments where historical data is marked unavailable: {has_unavailable}")

    print("\nAll API endpoint tests PASSED successfully!")

if __name__ == "__main__":
    test_endpoints()
