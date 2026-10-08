import urllib.request
import urllib.parse
import json
import sys

repos = [
    'Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025-Python---Jupyternotebook',
    'Saurabh-Vidyarthi/Classification_of_Indian_cities_based_on_road_accident_using_NDAP_Dataset',
    'rahul-saha18/India-Road-Accident-Exploratory-Data-Analysis.',
    'tajsohal2003/Road-accident-severity-analysis-',
    'Mayur0620/Road_Accidents_India',
    'shivadeatharva/Indian-Road-Data-Visualizer',
    'Ntabochrispine/Road-accident-predicting-model.'
]

for repo in repos:
    url = f"https://api.github.com/repos/{repo}/contents"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"=== Repo: {repo} ===")
            for item in data:
                print(f"  {item['name']} ({item['type']}, size: {item.get('size', 0)} bytes, download: {item.get('download_url')})")
    except Exception as e:
        print(f"Error {repo}: {e}")
