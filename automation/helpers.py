import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_today_fixtures():
    url = "https://www.flashscore.com./today-fixtures"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    fixtures = []

    # Örnek: her maç tr içinde
    for tr in soup.select("table.fixtures tr.match"):
        match_id = tr.get("data-id")
        league = tr.get("data-league")
        home = tr.select_one(".home").text.strip()
        away = tr.select_one(".away").text.strip()
        date = datetime.utcnow().strftime("%Y-%m-%d")
        fixtures.append({"id": match_id, "league": league, "homeTeam": home, "awayTeam": away, "date": date})
    return fixtures

def fetch_today_results():
    url = "https://www.example.com/today-results"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for tr in soup.select("table.results tr.match"):
        match_id = tr.get("data-id")
        score = tr.select_one(".score").text.strip()  # örn: 2-1
        results.append({"id": match_id, "score": score})
    return results
