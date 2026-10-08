import urllib.request
import urllib.parse
import json
import math
from typing import Dict, Any, List, Tuple

EARTH_RADIUS_KM = 6371.0

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(max(0, min(1, a))))
    return EARTH_RADIUS_KM * c

class OSRMRoutingClient:
    OSRM_URL = "https://router.project-osrm.org/route/v1/driving"
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

    @classmethod
    def geocode(cls, query: str) -> Tuple[float, float, str]:
        """
        Geocode city or place name in India using OpenStreetMap Nominatim.
        """
        q = query.strip()
        if not q.lower().endswith("india"):
            search_query = f"{q}, India"
        else:
            search_query = q

        params = urllib.parse.urlencode({"q": search_query, "format": "json", "limit": 1})
        url = f"{cls.NOMINATIM_URL}?{params}"
        req = urllib.request.Request(url, headers={'User-Agent': 'IndianAccidentRiskApp/1.0'})
        
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data:
                    lat = float(data[0]["lat"])
                    lon = float(data[0]["lon"])
                    display_name = data[0].get("display_name", query)
                    return lat, lon, display_name
        except Exception as e:
            print(f"Geocoding error for '{query}': {e}")
            
        # Common fallback Indian cities if Nominatim is rate-limited
        INDIAN_CITIES = {
            "delhi": (28.6139, 77.2090, "New Delhi, Delhi, India"),
            "mumbai": (19.0760, 72.8777, "Mumbai, Maharashtra, India"),
            "pune": (18.5204, 73.8567, "Pune, Maharashtra, India"),
            "bengaluru": (12.9716, 77.5946, "Bengaluru, Karnataka, India"),
            "bangalore": (12.9716, 77.5946, "Bengaluru, Karnataka, India"),
            "chennai": (13.0827, 80.2707, "Chennai, Tamil Nadu, India"),
            "hyderabad": (17.3850, 78.4867, "Hyderabad, Telangana, India"),
            "kolkata": (22.5726, 88.3639, "Kolkata, West Bengal, India"),
            "jaipur": (26.9124, 75.7873, "Jaipur, Rajasthan, India"),
            "chandigarh": (30.7333, 76.7794, "Chandigarh, India"),
            "bhubaneswar": (20.2961, 85.8245, "Bhubaneswar, Odisha, India"),
            "kolhapur": (16.7050, 74.2433, "Kolhapur, Maharashtra, India")
        }
        clean_key = q.lower().split(",")[0].strip()
        if clean_key in INDIAN_CITIES:
            lat, lon, name = INDIAN_CITIES[clean_key]
            return lat, lon, name
            
        raise ValueError(f"Could not geocode location: '{query}'")

    @classmethod
    def get_route(cls, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Dict[str, Any]:
        """
        Fetch real route from OSRM.
        Coordinates in URL are {lon},{lat}.
        """
        url = (
            f"{cls.OSRM_URL}/{start_lon:.6f},{start_lat:.6f};{end_lon:.6f},{end_lat:.6f}"
            f"?overview=full&geometries=geojson&steps=true"
        )
        req = urllib.request.Request(url, headers={'User-Agent': 'IndianAccidentRiskApp/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            # Fallback: simple straight‑line route when OSRM is unreachable
            # Generate 10 intermediate points between start and end
            num_pts = 10
            lat_step = (end_lat - start_lat) / (num_pts - 1)
            lon_step = (end_lon - start_lon) / (num_pts - 1)
            coords = []
            total_dist = 0.0
            prev = (start_lat, start_lon)
            for i in range(num_pts):
                lat = start_lat + lat_step * i
                lon = start_lon + lon_step * i
                coords.append([lon, lat])  # OSRM expects [lon, lat]
                if i > 0:
                    total_dist += haversine_km(prev[0], prev[1], lat, lon)
                    prev = (lat, lon)
            # Approximate duration assuming 60 km/h average speed
            duration = total_dist / 60.0 * 60.0
            route = {
                "geometry": {"coordinates": coords},
                "distance": total_dist * 1000,
                "duration": duration * 60,
                "legs": []
            }
            data = {"code": "Ok", "routes": [route]}
        
        if data.get("code") != "Ok" or not data.get("routes"):
            raise ValueError(f"OSRM routing failed: {data.get('code')}")
            
        route = data["routes"][0]
        coordinates = route["geometry"]["coordinates"] # list of [lon, lat]
        distance_km = round(route["distance"] / 1000.0, 1)
        duration_mins = round(route["duration"] / 60.0, 1)
        legs = route.get("legs", [])
        
        # Extract steps maneuvers to detect junctions and turn angles
        junction_coords = []
        for leg in legs:
            for step in leg.get("steps", []):
                maneuver = step.get("maneuver", {})
                loc = maneuver.get("location")
                if loc and maneuver.get("type") in ["turn", "fork", "roundabout", "intersection"]:
                    junction_coords.append((loc[1], loc[0])) # (lat, lon)
                    
        return {
            "coordinates": coordinates, # [ [lon, lat], ... ]
            "distance_km": distance_km,
            "duration_mins": duration_mins,
            "junction_coords": junction_coords
        }

    @classmethod
    def segment_route(cls, coordinates: List[List[float]], target_segment_len_km: float = 2.0) -> List[Dict[str, Any]]:
        """
        Split a polyline into discrete, consecutive segments of approximately target_segment_len_km.
        Each segment contains:
          - segment_index: int
          - start_coord: [lat, lon]
          - mid_coord: [lat, lon]
          - end_coord: [lat, lon]
          - coordinates: list of [lat, lon] for Leaflet polyline rendering
          - distance_km: float
        """
        if len(coordinates) < 2:
            return []

        segments = []
        current_segment_coords = []
        current_km = 0.0
        
        # Input coordinates are [lon, lat], convert to [lat, lon]
        pts = [(c[1], c[0]) for c in coordinates]
        current_segment_coords.append(pts[0])
        
        for i in range(1, len(pts)):
            prev_pt = pts[i - 1]
            curr_pt = pts[i]
            d = haversine_km(prev_pt[0], prev_pt[1], curr_pt[0], curr_pt[1])
            current_km += d
            current_segment_coords.append(curr_pt)
            
            if current_km >= target_segment_len_km or i == len(pts) - 1:
                mid_idx = len(current_segment_coords) // 2
                mid_pt = current_segment_coords[mid_idx]
                
                # Detect curvature by angle variance
                is_curve = False
                if len(current_segment_coords) >= 4:
                    angles = []
                    for j in range(1, len(current_segment_coords) - 1):
                        p0 = current_segment_coords[j - 1]
                        p1 = current_segment_coords[j]
                        p2 = current_segment_coords[j + 1]
                        b1 = math.atan2(p1[0] - p0[0], p1[1] - p0[1])
                        b2 = math.atan2(p2[0] - p1[0], p2[1] - p1[1])
                        angle_diff = abs(math.degrees(b2 - b1))
                        angles.append(angle_diff)
                    if angles and max(angles) > 35.0:
                        is_curve = True

                segments.append({
                    "segment_index": len(segments),
                    "coordinates": current_segment_coords,
                    "start_coord": current_segment_coords[0],
                    "mid_coord": mid_pt,
                    "end_coord": current_segment_coords[-1],
                    "distance_km": round(current_km, 2),
                    "is_curve": is_curve
                })
                
                # Start new segment from the end of the previous one
                current_segment_coords = [curr_pt]
                current_km = 0.0

        return segments
