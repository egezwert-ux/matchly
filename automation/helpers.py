import requests
from datetime import datetime

# Günün tarihini formatla
def get_today_date():
    return datetime.utcnow().strftime("%Y-%m-%d")

# Fixture ve sonuçları çekmek için tek endpoint kullanacağız
BASE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/"

def fetch_today_fixtures():
    date = get_today_date()
    url = f"{BASE_URL}{date}"
    resp = requests.get(url)
    data = resp.json()
    fixtures = []

    for event in data.get("events", []):
        home = event["homeTeam"]["name"]
        away = event["awayTeam"]["name"]
        fixtures.append({
            "id": str(event["id"]),
            "league": event["tournament"]["name"],
            "homeTeam": home,
            "awayTeam": away,
            "date": date
        })
    return fixtures

def fetch_today_results():
    date = get_today_date()
    url = f"{BASE_URL}{date}"
    resp = requests.get(url)
    data = resp.json()
    results = []

    for event in data.get("events", []):
        home_score = event.get("homeScore")
        away_score = event.get("awayScore")
        if home_score is not None and away_score is not None:
            score = f"{home_score}-{away_score}"
            results.append({"id": str(event["id"]), "score": score})
    return results
