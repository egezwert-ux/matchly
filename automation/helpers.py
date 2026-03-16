import requests
from datetime import datetime, timezone, timedelta

# Sofascore endpointleri
FIXTURE_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"
RESULTS_URL = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/{date}"

def fetch_today_fixtures():
    # Türkiye saati
    tr_time = datetime.now(timezone(timedelta(hours=3)))
    date_str = tr_time.strftime("%Y-%m-%d")

    url = FIXTURE_URL.format(date=date_str)
    try:
        resp = requests.get(url)
        data = resp.json()
        events = data.get("events", [])
        fixtures = []
        for e in events:
            fixtures.append({
                "id": str(e.get("id")),
                "league": e.get("tournament", {}).get("name", ""),
                "homeTeam": e.get("homeTeam", {}).get("name", ""),
                "awayTeam": e.get("awayTeam", {}).get("name", ""),
                "date": date_str
            })
        return fixtures
    except Exception as ex:
        print("Error fetching fixtures:", ex)
        return []

def fetch_today_results():
    # Türkiye saati
    tr_time = datetime.now(timezone(timedelta(hours=3)))
    date_str = tr_time.strftime("%Y-%m-%d")

    url = RESULTS_URL.format(date=date_str)
    try:
        resp = requests.get(url)
        data = resp.json()
        events = data.get("events", [])
        results = []
        for e in events:
            home_score = e.get("homeScore", "")
            away_score = e.get("awayScore", "")
            results.append({
                "id": str(e.get("id")),
                "score": f"{home_score}-{away_score}" if home_score != "" and away_score != "" else ""
            })
        return results
    except Exception as ex:
        print("Error fetching results:", ex)
        return []
