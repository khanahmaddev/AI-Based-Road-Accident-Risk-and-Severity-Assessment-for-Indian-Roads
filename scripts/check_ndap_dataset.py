import urllib.request
import json

url = 'https://api.github.com/repos/Saurabh-Vidyarthi/Classification_of_Indian_cities_based_on_road_accident_using_NDAP_Dataset/contents/Road_Accident_Classificaion/Dataset'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        for item in data:
            print(f"NDAP item: {item['name']} ({item['type']}, size: {item.get('size', 0)}, url: {item.get('download_url')})")
except Exception as e:
    print(e)
