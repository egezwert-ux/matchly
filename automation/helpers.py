# helpers.py
import requests
from datetime import datetime

# Örnek: Sofascore public JSON endpoint
# Bu endpointi kendi date ve lig filtrelerine göre değiştir
SOFASCORE_FIXTURE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"
SOFASCORE_RESULTS_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}/results"

def fetch_today_fixtures():
    """Bugünün maçlarını çek (fixture)"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = SOFASCORE_FIXTURE_URL.format(date=today)

    resp = requests.get(url)
    data = resp.json()

    fixtures = []
    for ev in data.get("events", []):
        fixtures.append({
            "id": str(ev["id"]),
            "league": ev["tournament"]["name"],
            "homeTeam": ev["homeTeam"]["name"],
            "awayTeam": ev["awayTeam"]["name"],
            "date": today
        })
    return fixtures

def fetch_today_results():
    """Bugünün maç sonuçlarını çek"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = SOFASCORE_RESULTS_URL.format(date=today)

    resp = requests.get(url)
    data = resp.json()

    results = []
    for ev in data.get("events", []):
        results.append({
            "id": str(ev["id"]),
            "score": f"{ev.get('homeScore',0)}-{ev.get('awayScore',0)}"
        })
    return results
