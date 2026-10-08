import os
import math
import numpy as np
import pandas as pd
from sklearn.neighbors import BallTree
from sklearn.cluster import DBSCAN

EARTH_RADIUS_METERS = 6371000.0

class SpatialAccidentIndex:
    _instance = None

    def __init__(self, data_path: str = None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "indian_roads_dataset.csv")
        
        self.data_path = data_path
        self.df = None
        self.tree = None
        self.coords_rad = None
        self.hotspots_cache = None
        self._load_and_index()

    def _load_and_index(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Accident dataset not found at {self.data_path}")
        
        print(f"Loading real Indian accident dataset from {self.data_path}...")
        df = pd.read_csv(self.data_path)
        # Ensure clean coordinates
        df = df.dropna(subset=['latitude', 'longitude']).copy()
        df['latitude'] = df['latitude'].astype(float)
        df['longitude'] = df['longitude'].astype(float)
        self.df = df.reset_index(drop=True)
        
        # Convert degrees to radians for BallTree with haversine metric
        # BallTree haversine expects coordinates as [latitude_rad, longitude_rad]
        lat_rad = np.radians(self.df['latitude'].values)
        lon_rad = np.radians(self.df['longitude'].values)
        self.coords_rad = np.column_stack((lat_rad, lon_rad))
        
        self.tree = BallTree(self.coords_rad, metric='haversine')
        print(f"Spatial index built successfully with {len(self.df)} verified incident points.")

    def query_radius(self, lat: float, lon: float, radius_meters: float = 2000.0, max_results: int = 50):
        """
        Query real accidents within radius_meters of (lat, lon).
        Returns dict with:
          - accidents: list of dicts
          - count: int
          - historical_data_available: bool
          - message: str
        """
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        radius_rad = radius_meters / EARTH_RADIUS_METERS
        
        # Query indices within radius
        indices, distances = self.tree.query_radius(
            [[lat_rad, lon_rad]], r=radius_rad, return_distance=True, sort_results=True
        )
        
        idx_list = indices[0]
        dist_list = distances[0] * EARTH_RADIUS_METERS # convert to meters
        
        accidents = []
        for i, idx in enumerate(idx_list[:max_results]):
            row = self.df.iloc[idx]
            accidents.append({
                "accident_id": int(row.get("accident_id", idx)),
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "severity": str(row.get("accident_severity", "unknown")),
                "date": str(row.get("date", "N/A")),
                "time": str(row.get("time", "N/A")),
                "road_type": str(row.get("road_type", "unknown")),
                "weather": str(row.get("weather", "unknown")),
                "cause": str(row.get("cause", "unknown")),
                "casualties": int(row.get("casualties", 0)) if pd.notnull(row.get("casualties")) else 0,
                "vehicles_involved": int(row.get("vehicles_involved", 1)) if pd.notnull(row.get("vehicles_involved")) else 1,
                "city": str(row.get("city", "N/A")),
                "state": str(row.get("state", "N/A")),
                "distance_meters": round(float(dist_list[i]), 1)
            })
            
        # Determine if real historical data is available in this geographical zone (within 15km)
        broad_radius_rad = 15000.0 / EARTH_RADIUS_METERS
        broad_count = len(self.tree.query_radius([[lat_rad, lon_rad]], r=broad_radius_rad)[0])
        has_coverage = broad_count > 0
        
        return {
            "accidents": accidents,
            "count": len(accidents),
            "historical_data_available": has_coverage,
            "message": "Historical accident data available" if has_coverage else "Historical accident data unavailable for this area."
        }

    def compute_hotspots(self, eps_meters: float = 1200.0, min_samples: int = 15):
        """
        Find real accident hotspots using DBSCAN clustering.
        """
        if self.hotspots_cache is not None:
            return self.hotspots_cache

        print("Computing verified accident hotspots using DBSCAN...")
        eps_rad = eps_meters / EARTH_RADIUS_METERS
        db = DBSCAN(eps=eps_rad, min_samples=min_samples, metric='haversine')
        cluster_labels = db.fit_predict(self.coords_rad)
        
        hotspots = []
        unique_labels = set(cluster_labels)
        
        for label in unique_labels:
            if label == -1:
                continue # Skip noise points
            
            mask = cluster_labels == label
            cluster_df = self.df[mask]
            
            center_lat = float(cluster_df['latitude'].mean())
            center_lon = float(cluster_df['longitude'].mean())
            total_count = int(len(cluster_df))
            
            sev_counts = cluster_df['accident_severity'].str.lower().value_counts().to_dict()
            fatal_count = int(sev_counts.get('fatal', 0))
            major_count = int(sev_counts.get('major', 0))
            minor_count = int(sev_counts.get('minor', 0))
            
            top_causes = cluster_df['cause'].value_counts().head(3).to_dict()
            cities = cluster_df['city'].unique().tolist()
            states = cluster_df['state'].unique().tolist()
            
            # Approximate radius in meters
            lats = np.radians(cluster_df['latitude'].values)
            lons = np.radians(cluster_df['longitude'].values)
            c_lat = math.radians(center_lat)
            c_lon = math.radians(center_lon)
            # Haversine distance from centroid
            dlat = lats - c_lat
            dlon = lons - c_lon
            a = np.sin(dlat/2)**2 + np.cos(c_lat) * np.cos(lats) * np.sin(dlon/2)**2
            c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
            max_dist_m = float(np.max(c) * EARTH_RADIUS_METERS)
            
            # Hotspot risk tier based on fatal and major accident ratio
            risk_score = min(100, int(35 + (fatal_count * 2.5) + (major_count * 1.2) + (total_count * 0.4)))
            
            hotspots.append({
                "hotspot_id": int(label),
                "latitude": round(center_lat, 6),
                "longitude": round(center_lon, 6),
                "radius_meters": round(max(max_dist_m, 300.0), 1),
                "total_accidents": total_count,
                "fatal_count": fatal_count,
                "major_count": major_count,
                "minor_count": minor_count,
                "risk_score": risk_score,
                "top_causes": top_causes,
                "cities": cities,
                "states": states
            })
            
        hotspots.sort(key=lambda h: h["risk_score"], reverse=True)
        self.hotspots_cache = hotspots
        print(f"Computed {len(hotspots)} verified accident hotspots across India.")
        return hotspots

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SpatialAccidentIndex()
        return cls._instance
