import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.osrm_client import OSRMRoutingClient
from backend.weather_client import WeatherClient
from backend.risk_engine import RiskEngine

def test():
    print("1. Geocoding Mumbai & Pune...")
    lat1, lon1, name1 = OSRMRoutingClient.geocode("Mumbai")
    lat2, lon2, name2 = OSRMRoutingClient.geocode("Pune")
    print(f"Start: {name1} ({lat1:.4f}, {lon1:.4f})")
    print(f"End:   {name2} ({lat2:.4f}, {lon2:.4f})")

    print("\n2. Fetching real OSRM route...")
    route = OSRMRoutingClient.get_route(lat1, lon1, lat2, lon2)
    print(f"Distance: {route['distance_km']} km, Duration: {route['duration_mins']} mins")

    print("\n3. Splitting route into segments...")
    segments = OSRMRoutingClient.segment_route(route['coordinates'], target_segment_len_km=10.0)
    print(f"Total segments: {len(segments)}")

    print("\n4. Running Risk Engine on first 3 segments with live weather...")
    engine = RiskEngine.get_instance()
    for seg in segments[:3]:
        mid_lat, mid_lon = seg["mid_coord"]
        weather = WeatherClient.get_live_weather(mid_lat, mid_lon)
        assessment = engine.assess_segment(
            lat=mid_lat,
            lon=mid_lon,
            weather=weather,
            road_infra={"road_type": "highway", "is_curve": seg["is_curve"]},
            temporal={"hour": 14}
        )
        print(f"Segment {seg['segment_index']} ({mid_lat:.4f}, {mid_lon:.4f}) -> Score: {assessment['risk_score']} ({assessment['risk_tier']}), Hist Accidents: {assessment['historical_accidents_count']}")
        print(f"  Color: {assessment['color']}, Historical Data Available: {assessment['historical_data_available']}")

if __name__ == "__main__":
    test()
