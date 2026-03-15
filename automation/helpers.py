import requests
from bs4 import BeautifulSoup
from datetime import datetime

# SofaScore fixtures ve results sayfaları
FIXTURE_URL = "https://www.sofascore.com/football/england/premier-league/fixtures"
RESULTS_URL = "https://www.sofascore.com/football/england/premier-league/results"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_today_fixtures():
    resp = requests.get(FIXTURE_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    fixtures = []

    # 🏟️ Her maç div'i
    for div in soup.select("div.event-row"):
        home = div.select_one(".home .name")
        away = div.select_one(".away .name")
        match_id = div.get("id")  # genellikle uniq id attribute
        league = "Premier League"  # Bu örnek, dilersen siteye göre alabilirsin

        if not home or not away:
            continue

        fixtures.append({
            "id": match_id,
            "league": league,
            "homeTeam": home.text.strip(),
            "awayTeam": away.text.strip(),
            "date": datetime.utcnow().strftime("%Y-%m-%d")
        })
    return fixtures

def fetch_today_results():
    resp = requests.get(RESULTS_URL, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for div in soup.select("div.event-row"):
        match_id = div.get("id")
        score_span = div.select_one(".score")  # skor div/span
        score = score_span.text.strip() if score_span else None

        if not match_id or not score:
            continue

        results.append({
            "id": match_id,
            "score": score
        })

    return results
