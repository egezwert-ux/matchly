import requests
from bs4 import BeautifulSoup
from datetime import datetime

SOFASCORE_FIXTURE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"

def fetch_today_fixtures():
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    url = SOFASCORE_FIXTURE_URL.format(date=today_str)
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        data = resp.json()
        fixtures = []
        for match in data.get("events", []):
            fixtures.append({
                "id": str(match.get("id")),
                "league": match.get("tournament", {}).get("name", ""),
                "homeTeam": match.get("homeTeam", {}).get("name", ""),
                "awayTeam": match.get("awayTeam", {}).get("name", ""),
                "date": today_str
            })
        return fixtures
    except Exception as e:
        print("Error fetching fixtures:", e)
        return []
