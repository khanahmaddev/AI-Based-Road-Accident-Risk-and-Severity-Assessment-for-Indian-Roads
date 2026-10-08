import urllib.request
import json
import os

def search_github():
    queries = [
        "indian road accident dataset",
        "india accident severity dataset",
        "road accidents india csv",
        "bangalore accident dataset csv",
        "delhi accident dataset csv"
    ]
    
    seen = set()
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                print(f"=== Query: {q} (Total: {data.get('total_count', 0)}) ===")
                for item in data.get('items', [])[:5]:
                    name = item['full_name']
                    if name not in seen:
                        seen.add(name)
                        print(f"Repo: {name} (Stars: {item['stargazers_count']})")
                        print(f"  Description: {item.get('description')}")
                        print(f"  URL: {item.get('html_url')}")
        except Exception as e:
            print(f"Error querying {q}: {e}")

if __name__ == "__main__":
    search_github()
